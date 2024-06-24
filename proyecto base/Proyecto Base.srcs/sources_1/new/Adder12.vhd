
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity Adder12 is
    Port ( a  : in  std_logic_vector (11 downto 0);
           b  : in  std_logic_vector (11 downto 0);
           ci : in  std_logic;
           s  : out std_logic_vector (15 downto 0);
           co : out std_logic);
end Adder12;

architecture Behavioral of Adder12 is

component FA
    Port ( a  : in  std_logic;
           b  : in  std_logic;
           ci : in  std_logic;
           s  : out std_logic;
           co : out std_logic);
    end component;

signal c : std_logic_vector(14 downto 0);
signal an: std_logic_vector(15 downto 0);
signal bn: std_logic_vector(15 downto 0);

begin

an <= "0000" & a;
bn <= "0000" & b;

inst_FA0: FA port map(
        a      =>an(0),
        b      =>bn(0),
        ci     =>ci,
        s      =>s(0),
        co     =>c(0)
    );
    
inst_FA1: FA port map(
        a      =>an(1),
        b      =>bn(1),
        ci     =>c(0),
        s      =>s(1),
        co     =>c(1)
    );

inst_FA2: FA port map(
        a      =>an(2),
        b      =>bn(2),
        ci     =>c(1),
        s      =>s(2),
        co     =>c(2)
    );

inst_FA3: FA port map(
        a      =>an(3),
        b      =>bn(3),
        ci     =>c(2),
        s      =>s(3),
        co     =>c(3)
    );

inst_FA4: FA port map(
        a      =>an(4),
        b      =>bn(4),
        ci     =>c(3),
        s      =>s(4),
        co     =>c(4)
    );
    
inst_FA5: FA port map(
        a      =>an(5),
        b      =>bn(5),
        ci     =>c(4),
        s      =>s(5),
        co     =>c(5)
    );

inst_FA6: FA port map(
        a      =>an(6),
        b      =>bn(6),
        ci     =>c(5),
        s      =>s(6),
        co     =>c(6)
    );

inst_FA7: FA port map(
        a      =>an(7),
        b      =>bn(7),
        ci     =>c(6),
        s      =>s(7),
        co     =>c(7)
    );
    
inst_FA8: FA port map(
        a      =>an(8),
        b      =>bn(8),
        ci     =>c(7),
        s      =>s(8),
        co     =>c(8)
    );
    
inst_FA9: FA port map(
        a      =>an(9),
        b      =>bn(9),
        ci     =>c(8),
        s      =>s(9),
        co     =>c(9)
    );

inst_FA10: FA port map(
        a      =>an(10),
        b      =>bn(10),
        ci     =>c(9),
        s      =>s(10),
        co     =>c(10)
    );

inst_FA11: FA port map(
        a      =>an(11),
        b      =>bn(11),
        ci     =>c(10),
        s      =>s(11),
        co     =>c(11)
    );

inst_FA12: FA port map(
        a      =>an(12),
        b      =>bn(12),
        ci     =>c(11),
        s      =>s(12),
        co     =>c(12)
    );
    
inst_FA13: FA port map(
        a      =>an(13),
        b      =>bn(13),
        ci     =>c(12),
        s      =>s(13),
        co     =>c(13)
    );

inst_FA14: FA port map(
        a      =>an(14),
        b      =>bn(14),
        ci     =>c(13),
        s      =>s(14),
        co     =>c(14)
    );

inst_FA15: FA port map(
        a      =>an(15),
        b      =>bn(15),
        ci     =>c(14),
        s      =>s(15),
        co     =>co
    );
    
end Behavioral;
