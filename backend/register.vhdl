library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity register_8bit is
    Port ( 
        clk     : in  STD_LOGIC;
        reset   : in  STD_LOGIC;
        load_en : in  STD_LOGIC; -- Controls when to store the result
        d       : in  STD_LOGIC_VECTOR (7 downto 0);
        q       : out STD_LOGIC_VECTOR (7 downto 0)
    );
end register_8bit;

architecture Behavioral of register_8bit is
begin
    process(clk, reset)
    begin
        -- Asynchronous active-high reset
        if reset = '1' then
            q <= (others => '0');
        -- Synchronous load
        elsif rising_edge(clk) then
            if load_en = '1' then
                q <= d;
            end if;
        end if;
    end process;
end Behavioral;