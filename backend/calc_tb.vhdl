library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity calculator_tb is
end calculator_tb;

architecture Behavioral of calculator_tb is

    -- =========================
    -- INPUTS (FROM BACKEND)
    -- =========================
    signal A_sig        : std_logic_vector(7 downto 0);
    signal B_sig        : std_logic_vector(7 downto 0);
    signal Op_sig       : std_logic_vector(1 downto 0);
    signal Display_sig  : std_logic := '0';

    -- OUTPUTS
    signal Main_Out_sig : std_logic_vector(7 downto 0);
    signal Err_sig      : std_logic;

begin

    -- =========================
    -- DEVICE UNDER TEST
    -- =========================
    DUT: entity work.calculator_top
        port map (
            A_top           => A_sig,
            B_top           => B_sig,
            Op_top          => Op_sig,
            Display_Sel_top => Display_sig,
            Main_Out_top    => Main_Out_sig,
            Err_out         => Err_sig
        );

    -- =========================
    -- MAIN TEST PROCESS
    -- =========================
    process
    begin

        -- =====================================
        -- WAIT FOR BACKEND INPUT ASSIGNMENT
        -- =====================================

        wait for 1 ns;  -- allow backend to assign values

        -- apply inputs already set by backend
        -- (no file, no loop, no clock)

        -- simple stabilization delay
        wait for 5 ns;

        -- =========================
        -- END SIMULATION CLEANLY
        -- =========================
        wait;
    end process;

end Behavioral;