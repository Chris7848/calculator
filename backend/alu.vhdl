library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity alu is
    Port ( 
        A           : in  STD_LOGIC_VECTOR (7 downto 0);
        B           : in  STD_LOGIC_VECTOR (7 downto 0);
        Op          : in  STD_LOGIC_VECTOR (1 downto 0);
        Display_Sel : in  STD_LOGIC; -- '0' = Result, '1' = Remainder/Overflow
        Main_Out    : out STD_LOGIC_VECTOR (7 downto 0);
        Error       : out STD_LOGIC
    );
end alu;

architecture Behavioral of alu is
begin
    process(A, B, Op, Display_Sel)
        variable temp_A, temp_B : unsigned(7 downto 0);
        variable v_Result       : std_logic_vector(7 downto 0);
        variable v_Extra        : std_logic_vector(7 downto 0);
        variable v_Error        : std_logic;
        
        -- Internal math variables
        variable sum_ext  : unsigned(8 downto 0);
        variable prod_ext : unsigned(15 downto 0);
    begin
        temp_A := unsigned(A);
        temp_B := unsigned(B);
        
        -- Default values to prevent unintended latches during synthesis
        v_Error  := '0';
        v_Result := (others => '0');
        v_Extra  := (others => '0');

        case Op is
            when "00" => -- Addition
                sum_ext  := ("0" & temp_A) + ("0" & temp_B);
                v_Result := std_logic_vector(sum_ext(7 downto 0));
                v_Error  := sum_ext(8); -- The Carry Flag
                v_Extra  := "0000000" & sum_ext(8);

            when "01" => -- Subtraction
                if temp_B > temp_A then 
                    v_Error := '1'; -- Underflow/Negative Error
                end if;
                v_Result := std_logic_vector(temp_A - temp_B);
                v_Extra  := (others => '0');

            when "10" => -- Multiplication
                prod_ext := temp_A * temp_B;
                v_Result := std_logic_vector(prod_ext(7 downto 0));
                v_Extra  := std_logic_vector(prod_ext(15 downto 8)); -- High Byte
                if prod_ext(15 downto 8) /= x"00" then 
                    v_Error := '1'; -- Result exceeds 8 bits
                end if;

            when "11" => -- Division
                if temp_B = x"00" then 
                    v_Error  := '1'; -- Divide by zero error
                    v_Result := (others => '1'); -- Output Max value (255) on error
                    v_Extra  := (others => '0');
                else 
                    v_Result := std_logic_vector(temp_A / temp_B);
                    v_Extra  := std_logic_vector(temp_A rem temp_B); -- Remainder
                end if;

            when others => 
                -- Safety catch, though 2-bit Op code makes this impossible to reach
                null;
        end case;

        -- Output Routing based on Display_Sel
        Error <= v_Error;
        
        if Display_Sel = '1' then
            Main_Out <= v_Extra;
        else
            Main_Out <= v_Result;
        end if;

    end process;
end Behavioral;