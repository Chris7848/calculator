library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity calculator_top is
    Port ( 
        A_top           : in  STD_LOGIC_VECTOR (7 downto 0);
        B_top           : in  STD_LOGIC_VECTOR (7 downto 0);
        Op_top          : in  STD_LOGIC_VECTOR (1 downto 0);
        Display_Sel_top : in  STD_LOGIC;

        Main_Out_top    : out STD_LOGIC_VECTOR (7 downto 0);
        Err_out         : out STD_LOGIC
    );
end calculator_top;

architecture Structural of calculator_top is
begin

    -- Direct ALU connection (NO REGISTER, NO CLOCK)
    ALU_UNIT: entity work.alu
        port map (
            A           => A_top,
            B           => B_top,
            Op          => Op_top,
            Display_Sel => Display_Sel_top,
            Main_Out    => Main_Out_top,
            Error       => Err_out
        );

end Structural;