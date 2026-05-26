library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use std.textio.all;

entity calculator_tb is
end calculator_tb;

architecture Behavioral of calculator_tb is

    signal A_sig       : std_logic_vector(7 downto 0);
    signal B_sig       : std_logic_vector(7 downto 0);
    signal Op_sig      : std_logic_vector(1 downto 0);
    signal Display_sig : std_logic := '0';

    signal Main_Out_sig : std_logic_vector(7 downto 0);
    signal Err_sig      : std_logic;

    file input_file  : text open read_mode is "input.txt";
    file output_file : text open write_mode is "output.txt";

begin

    DUT: entity work.calculator_top
        port map (
            A_top           => A_sig,
            B_top           => B_sig,
            Op_top          => Op_sig,
            Display_Sel_top => Display_sig,
            Main_Out_top    => Main_Out_sig,
            Err_out         => Err_sig
        );

    process
        variable line_in  : line;
        variable line_out : line;
        variable vA, vB, vOp, vDisp : integer;
    begin

        -- wait for backend to write file
        wait for 100 ns;

        -- read inputs
        readline(input_file, line_in); read(line_in, vA);
        readline(input_file, line_in); read(line_in, vB);
        readline(input_file, line_in); read(line_in, vOp);
        readline(input_file, line_in); read(line_in, vDisp);

        -- assign signals
        A_sig  <= std_logic_vector(to_unsigned(vA, 8));
        B_sig  <= std_logic_vector(to_unsigned(vB, 8));
        Op_sig <= std_logic_vector(to_unsigned(vOp, 2));

        if vDisp = 1 then
            Display_sig <= '1';
        else
            Display_sig <= '0';
        end if;

        wait for 20 ns;

        -- write output
        write(line_out, to_integer(unsigned(Main_Out_sig)));
        writeline(output_file, line_out);

        wait;
    end process;

end Behavioral;
