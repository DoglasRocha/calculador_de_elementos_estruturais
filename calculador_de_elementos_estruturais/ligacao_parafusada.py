from .pegador_parafusada import PegadorParafusada
from .calculador_parafusada import CalculadorParafusada
from .informacoes import request_resistencia_chapas, request_resistencia_parafuso

class LigacaoParafusada:
    def __init__(self):
        '''cantoneira'''
        self.medida_aba_cantoneira = PegadorParafusada.pega_medida('Insira a medida em mm da aba da cantoneira. ')
        self.espessura_cantoneira = PegadorParafusada.pega_espessura('Insira a espessura em mm da cantoneira. ')
        
        '''fu e fy parafuso'''
        self.diametro_parafuso = PegadorParafusada.pega_diametro_parafuso()
        self.especificacao_parafuso = PegadorParafusada.pega_especificacao_parafuso()
        self.fy_parafuso, self.fu_parafuso = request_resistencia_parafuso(self.especificacao_parafuso, 
                                                                          self.diametro_parafuso) if self.especificacao_parafuso != 'Outro' else PegadorParafusada.pega_fy_e_fu('o parafuso')
        
        '''fu e fy chapa'''
        self.especificacao_chapa = PegadorParafusada.pega_especificacao_chapa()
        self.fy_chapa, self.fu_chapa = request_resistencia_chapas(self.especificacao_chapa) if self.especificacao_chapa != 'Outro' else PegadorParafusada.pega_fy_e_fu('a chapa')
        
        '''cantoneira'''
        self.area_bruta_cantoneira = CalculadorParafusada.calcula_area_bruta_cantoneira(self.medida_aba_cantoneira, 
                                                                                        self.espessura_cantoneira)
        self.largura_bruta_cantoneira = CalculadorParafusada.calcula_largura_bruta_cantoneira(self.medida_aba_cantoneira, 
                                                                                              self.espessura_cantoneira)
        self.largura_liquida_cantoneira = CalculadorParafusada.calcula_largura_liquida(self.largura_bruta_cantoneira, 
                                                                                       self.diametro_parafuso, 
                                                                                       0.35)
        self.area_liquida_cantoneira = CalculadorParafusada.calcula_area_liquida(self.largura_liquida_cantoneira, 
                                                                                 self.espessura_cantoneira)
        self.resistencia_tracao_cantoneira_secao_bruta = CalculadorParafusada.calcula_resistencia_tracao_secao_bruta(self.area_bruta_cantoneira, 
                                                                                                                     self.fy_chapa)
        self.resistencia_tracao_cantoneira_secao_liquida = CalculadorParafusada.calcula_resistencia_tracao_secao_liquida(self.area_liquida_cantoneira, 
                                                                                                                         self.fu_chapa)
        self.resistencia_tracao_cantoneira = self.seleciona_menor_valor(self.resistencia_tracao_cantoneira_secao_bruta, 
                                                                              self.resistencia_tracao_cantoneira_secao_liquida)
        
        '''gusset'''
        self.medida_gusset = PegadorParafusada.pega_medida('Insira o comprimento em mm do Gusset(z). ')
        self.espessura_gusset = PegadorParafusada.pega_espessura('Insira a espessura em mm do Gusset. ')
        
        self.area_bruta_gusset = CalculadorParafusada.calcula_area_bruta_gusset(self.medida_gusset, 
                                                                                self.espessura_gusset)
        self.largura_liquida_gusset = CalculadorParafusada.calcula_largura_liquida(self.medida_gusset, 
                                                                                   self.diametro_parafuso, 
                                                                                   0.35)
        self.area_liquida_gusset = CalculadorParafusada.calcula_area_liquida(self.largura_liquida_gusset, 
                                                                             self.espessura_gusset)
        self.resistencia_tracao_gusset_secao_bruta = CalculadorParafusada.calcula_resistencia_tracao_secao_bruta(self.area_bruta_gusset, 
                                                                                                                 self.fy_chapa)
        self.resistencia_tracao_gusset_secao_liquida = CalculadorParafusada.calcula_resistencia_tracao_secao_liquida(self.area_liquida_gusset, 
                                                                                                                     self.fu_chapa, 1)
        self.resistencia_tracao_gusset = self.seleciona_menor_valor(self.resistencia_tracao_gusset_secao_bruta, 
                                                                          self.resistencia_tracao_gusset_secao_liquida)
        
        '''pressao de contato nas cantoneiras'''
        self.distancia_furos = PegadorParafusada.pega_medida('Informe a dist??ncia em mm entre os centros dos furos. ')
        self.dist_lado_esquerdo = PegadorParafusada.pega_medida('Informe a medida em mm de a. ')
        self.dist_lado_direito = PegadorParafusada.pega_medida('Informe a medida em mm de c. ')
        self.qtd_parafusos = PegadorParafusada.pega_quantidade_parafusos()
        self.e = self.seleciona_menor_valor(self.dist_lado_direito, 
                                            self.dist_lado_esquerdo)
        
        self.pressao_centro_centro_furos = CalculadorParafusada.calcula_pressao_centro_furos(self.distancia_furos, 
                                                                                             self.diametro_parafuso)
        self.pressao_centro_furo_bordo = CalculadorParafusada.calcula_pressao_centro_furo_bordo(self.e, 
                                                                                                self.diametro_parafuso)
        self.pressao_rasgamento_chapa = self.seleciona_menor_valor(self.pressao_centro_centro_furos, 
                                                                   self.pressao_centro_furo_bordo)
        self.pressao_esmagamento_chapa = CalculadorParafusada.calcula_esmagamento_chapa(self.pressao_rasgamento_chapa,
                                                                                        self.qtd_parafusos,
                                                                                        self.diametro_parafuso,
                                                                                        self.espessura_cantoneira,
                                                                                        self.fu_chapa)
        
        '''Resist??ncia ao cisalhamento nos parafusos'''
        self.resistencia_cisalhamento_parafusos = CalculadorParafusada.calcula_resistencia_cisalhamento_parafusos(self.diametro_parafuso, 
                                                                                                                  self.fu_parafuso, 
                                                                                                                  self.qtd_parafusos)
        
        '''M??ximo Esfor??o Nominal'''
        self.resistencia_ligacao = self.seleciona_menor_valor(self.resistencia_tracao_cantoneira,
                                                              self.resistencia_tracao_gusset,
                                                              self.pressao_esmagamento_chapa,
                                                              self.resistencia_cisalhamento_parafusos)
        self.maximo_esforco_nominal = CalculadorParafusada.calcula_maximo_esforco_nominal(self.resistencia_ligacao)
        
        '''impress??o dos valores'''
        print(self)
        
    @staticmethod        
    def seleciona_menor_valor(*args):
        menor_valor = min(args)
        return menor_valor

    def __str__(self):
        abre_negrito = '\033[1m'
        fecha_negrito = '\033[0m'
        n = abre_negrito
        _n = fecha_negrito
        
        impressao = f'''

        {n}Liga????o Parafusada
        
            {n}Cantoneira
        
    {n}1) Tra????o na Cantoneira
    
        {n}1.1) C??lculo da ??rea bruta da cantoneira
        
{n}??rea Bruta da cantoneira (Ag){_n}: {round(self.area_bruta_cantoneira, 6)} cm??

        {n}1.2) C??lculo da ??rea l??quida na se????o normal
        
{n}Largura bruta da cantoneira(bg){_n}: {round(self.largura_bruta_cantoneira, 6)} cm
{n}Largura l??quida da cantoneira (bn){_n}: {round(self.largura_liquida_cantoneira, 6)} cm
{n}??rea l??quida da cantoneira (An){_n}: {round(self.area_liquida_cantoneira, 6)} cm??

        {n}1.3) Resist??ncia da cantoneira ?? tra????o na se????o bruta
        
{n}Resist??ncia (?? * Nn){_n}: {round(self.resistencia_tracao_cantoneira_secao_bruta, 6)} N

        {n}1.4) Resist??ncia da cantoneira ?? tra????o na se????o com furos
        
{n}Resist??ncia (?? * Nn){_n}: {round(self.resistencia_tracao_cantoneira_secao_liquida, 6)} N

    {n}Resist??ncia ?? tra????o na cantoneira (?? * Nn){_n}: {round(self.resistencia_tracao_cantoneira, 6)} N
    
            {n}Gusset
            
    {n}2) Tra????o no Gusset
    
        {n}2.1) C??lculo da ??rea bruta
        
{n}??rea Bruta do Gusset (Ag){_n}: {round(self.area_bruta_gusset, 6)} cm??

        {n}2.2) C??lculo da ??rea l??quina na se????o normal
        
{n}Largura L??quida Gusset (bn){_n}: {round(self.largura_liquida_gusset, 6)} cm
{n}??rea L??quida Gusset {_n}{_n}: {round(self.area_liquida_gusset, 6)} cm??

        {n}2.3) Resist??ncia ?? tra????o na se????o bruta do Gusset
        
{n}Resist??ncia (?? * Nn){_n}: {round(self.resistencia_tracao_gusset_secao_bruta, 6)} N

        {n}2.4) Resist??ncia ?? tra????o na se????o com futos do Gusset
        
{n}Resist??ncia (?? * Nn){_n}: {round(self.resistencia_tracao_gusset_secao_liquida, 6)} N

    {n}Resist??ncia ?? tra????o no Gusset (?? * Nn){_n}: {round(self.resistencia_tracao_gusset, 6)} N
    
            {n}Contato nas cantoneiras
    
    {n}3) Press??o de contato na cantoneira
            
        {n}3.1) Rasgamento da chapa
        
{n}Centro a centro furos (??s){_n}: {round(self.pressao_centro_centro_furos, 6)}
{n}Centro do furo ao bordo (??e){_n}:{round(self.pressao_centro_furo_bordo, 6)}
{n}Rasgamento da chapa (??){_n}: {round(self.pressao_rasgamento_chapa, 6)}

        {n}3.2) Esmagamento da chapa
        
{n}Press??o de Esmagamento da chapa (?? * Nn){_n}: {round(self.pressao_esmagamento_chapa, 6)} N

            {n}Cisalhamento nos parafusos

    {n}4) Resist??ncia ao cisalhamento nos parafusos
        
{n}Resist??ncia (?? * Nn){_n}: {round(self.resistencia_cisalhamento_parafusos, 6)} N

        {n}5) C??lculo do M??ximo Esfor??o Nominal
        
{n}Resist??ncia de liga????o (Nd){_n}: {round(self.resistencia_ligacao, 6)} N

{n}M??ximo Esfor??o Nominal (N){_n}: {round(self.maximo_esforco_nominal, 6)} N

'''

        return impressao