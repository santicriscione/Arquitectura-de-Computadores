library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.std_logic_unsigned.all;
use IEEE.numeric_std.all;


entity CPU is
    Port (
           clock : in STD_LOGIC;
           clear : in STD_LOGIC;
           ram_address : out STD_LOGIC_VECTOR (11 downto 0);
           ram_datain : out STD_LOGIC_VECTOR (15 downto 0);
           ram_dataout : in STD_LOGIC_VECTOR (15 downto 0);
           ram_write : out STD_LOGIC;
           rom_address : out STD_LOGIC_VECTOR (11 downto 0);
           rom_dataout : in STD_LOGIC_VECTOR (35 downto 0));
end CPU;

architecture Behavioral of CPU is

component Reg
    Port ( clock    : in  std_logic;                        -- Señal del clock (reducido).
           clear    : in  std_logic;                        -- Señal de reset.
           load     : in  std_logic;                        -- Señal de carga.
           up       : in  std_logic;                        -- Señal de subida.
           down     : in  std_logic;                        -- Señal de bajada.
           datain   : in  std_logic_vector (15 downto 0);   -- Señales de entrada de datos.
           dataout  : out std_logic_vector (15 downto 0));
    end component;

component Status 
    Port ( clock    : in  std_logic;                        -- Señal del clock (reducido).
           clear    : in  std_logic;                        -- Señal de reset.
           load     : in  std_logic;                        -- Señal de carga.
           up       : in  std_logic;                        -- Señal de subida.
           down     : in  std_logic;                        -- Señal de bajada.
           datain   : in  std_logic_vector (2 downto 0);   -- Señales de entrada de datos.
           dataout  : out std_logic_vector (2 downto 0));
     end component;
     
 component PC
        Port ( clock    : in  std_logic;                        -- Señal del clock (reducido).
           clear    : in  std_logic;                        -- Señal de reset.
           load     : in  std_logic;                        -- Señal de carga.
           up       : in  std_logic;                        -- Señal de subida.
           down     : in  std_logic;                        -- Señal de bajada.
           datain   : in  std_logic_vector (11 downto 0);   -- Señales de entrada de datos.
           dataout  : out std_logic_vector (11 downto 0));
      end component;
      
 component ALU 
     Port ( a        : in  std_logic_vector (15 downto 0);   -- Primer operando.
           b        : in  std_logic_vector (15 downto 0);   -- Segundo operando.
           sop      : in  std_logic_vector (2 downto 0);   -- Selector de la operación.
           c        : out std_logic;                       -- Señal de 'carry'.
           z        : out std_logic;                       -- Señal de 'zero'.
           n        : out std_logic;                       -- Señal de 'nagative'.
           result   : out std_logic_vector (15 downto 0));
     end component;
     
 component ControlUnit
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
           selPC: out std_logic
           );
    end component;

 component SP
        Port ( clock    : in  std_logic;                        -- Señal del clock (reducido).
           clear    : in  std_logic;                        -- Señal de reset.
           load     : in  std_logic;                        -- Señal de carga.
           up       : in  std_logic;                        -- Señal de subida.
           down     : in  std_logic;                        -- Señal de bajada.
           datain   : in  std_logic_vector (11 downto 0);   -- Señales de entrada de datos.
           dataout  : out std_logic_vector (11 downto 0));
      end component;
      
component Adder12 is
    Port ( a  : in  std_logic_vector (11 downto 0);
           b  : in  std_logic_vector (11 downto 0);
           ci : in  std_logic;
           s  : out std_logic_vector (15 downto 0);
           co : out std_logic);
end component;
      
signal status_result: std_logic_vector(2 downto 0);
signal muxA_out: std_logic_vector(15 downto 0);
signal muxB_out: std_logic_vector(15 downto 0);
signal s_enableA: STD_LOGIC;
signal s_enableB: STD_LOGIC;
signal s_selA : STD_LOGIC_VECTOR (1 downto 0);
signal s_selB : STD_LOGIC_VECTOR (1 downto 0);
signal s_selALU : STD_LOGIC_VECTOR (2 downto 0);
signal s_loadPC : STD_LOGIC;
signal s_w : STD_LOGIC;
signal ALU_result: std_logic_vector(15 downto 0);
signal z_signal: STD_LOGIC;
signal c_signal: STD_LOGIC;
signal n_signal: STD_LOGIC;
signal regA_out: std_logic_vector(15 downto 0);
signal regB_out: std_logic_vector(15 downto 0);
signal status_bus: std_logic_vector(2 downto 0);
signal data_PC: std_logic_vector(11 downto 0);
signal s_selPC: std_logic;
signal s_incSP: std_logic;
signal s_decSP: std_logic;
signal s_selAdd: std_logic_vector(1 downto 0);
signal s_selDin: std_logic;
signal SP_data: std_logic_vector(11 downto 0);
signal out_PC: std_logic_vector (11 downto 0);
signal Adder_result: std_logic_vector(15 downto 0);
signal SP_datain: std_logic_vector(11 downto 0);

begin

inst_RegA: Reg port map(
    clock => clock,
    clear => clear,
    load => s_enableA,
    up => '0',
    down => '0',
    datain => ALU_result,
    dataout => regA_out
);

inst_RegB: Reg port map(
    clock => clock,
    clear => clear,
    load => s_enableB,
    up => '0',
    down => '0',
    datain => ALU_result,
    dataout => regB_out
);

with s_selA select 
    muxA_out <= "0000000000000000" when "00",
                "0000000000000001" when "01",
                regA_out when "10",
                "0000000000000000" when others;
                
with s_selB select 
    muxB_out <= "0000000000000000" when "00",
                ram_dataout when "10",
                regB_out when "01",
                rom_dataout(15 downto 0) when "11",
                "0000000000000000" when others;

inst_ALU: ALU port map(
    a => muxA_out,
    b => muxB_out,
    sop => s_selALU,
    z => z_signal,
    c => c_signal,
    n => n_signal,
    result => ALU_result
);

status_bus <= c_signal & z_signal & n_signal;

inst_Status: Status port map(
    clock => clock,
    clear => clear,
    load => '1',
    up => '0',
    down => '0',
    datain => status_bus,
    dataout => status_result
);

ints_ControlUnit: ControlUnit port map(
    opcode => rom_dataout(35 downto 16),
    status => status_result,
    enableA => s_enableA,
    enableB => s_enableB,
    selA => s_selA,
    selB => s_selB,
    selALU => s_selALU,
    loadPC => s_loadPC,
    w => s_w,
    inc_SP => s_incSP,
    dec_SP => s_decSP,
    selAdd => s_selAdd,
    selDin => s_selDin,
    selPC => s_selPC);

with s_selPC select
    data_PC <= rom_dataout(11 downto 0) when '0',
               ram_dataout(11 downto 0) when '1',
               "000000000000" when others;

inst_PC: PC port map(
    clock => clock,
    clear => clear,
    load => s_loadPC,
    up => '1',
    down => '0',
    datain => data_PC,
    dataout => out_PC
);

rom_address <= out_PC;
    
inst_SP: SP port map(
    clock => clock,
    clear => clear,
    load => '0',
    up => s_incSP,
    down => s_decSP,
    datain => "000000000000",
    dataout => SP_data
);

with s_selAdd select
    ram_address <= SP_data when "00",
                   rom_dataout(11 downto 0) when "01",
                   regB_out(11 downto 0) when "10",
                   "000000000000" when others;
                   
inst_Adder12: Adder12 port map(
    a => "000000000001",
    b => out_PC,
    ci => '0',
    s => Adder_result);
    
with s_selDin select
    ram_datain <= alu_result when '0',
                  Adder_result when '1';
                  
ram_write <= s_w;
end Behavioral;

