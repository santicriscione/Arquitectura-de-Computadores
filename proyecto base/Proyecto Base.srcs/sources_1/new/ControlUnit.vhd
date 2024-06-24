

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity ControlUnit is
    Port ( opcode : in STD_LOGIC_VECTOR (19 downto 0);
           status : in STD_LOGIC_VECTOR (2 downto 0);
           enableA: out STD_LOGIC;
           enableB: out STD_LOGIC;
           selA : out STD_LOGIC_VECTOR (1 downto 0);
           selB : out STD_LOGIC_VECTOR (1 downto 0);
           selALU : out STD_LOGIC_VECTOR (2 downto 0);
           loadPC : out STD_LOGIC;
           w : out STD_LOGIC;
           inc_SP: out std_logic;
           dec_SP: out std_logic;
           selAdd: out std_logic_vector (1 downto 0);
           selDin: out std_logic;
           selPC: out std_logic);
end ControlUnit;

architecture Behavioral of ControlUnit is

signal c: STD_LOGIC;
signal z: STD_LOGIC;
signal n: STD_LOGIC;
signal sel_jump: std_logic_vector(2 downto 0);
signal pc: std_logic;

begin

c <= status(2);
z <= status(1);
n <= status(0);
sel_jump <= opcode(13 downto 11);

with sel_jump select 
    pc <= '1' when "000",
              z  when "001", 
              not z when "010",
              (not n) and (not z) when "011",
              not n  when "100",
              n when "101",
              n or z when "110",
              c when "111",
              '0' when others;     
                      
selAdd <= opcode(19 downto 18);
selDin <= opcode(17);
selPC <= opcode(16);
inc_SP <= opcode(15);
dec_SP <= opcode(14);
enableA <= opcode(10);
enableB <= opcode(9);
selA <= opcode(8 downto 7);
selB <= opcode(6 downto 5);
selALU <= opcode(4 downto 2);
loadPC <= opcode(1)and pc;
w <= opcode(0);


end Behavioral;
