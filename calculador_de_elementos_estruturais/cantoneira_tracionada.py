from pegador_parafusada import PegadorParafusada
from calculador_cantoneira_tracionada import CalculadorCantoneiraTracionada
from informacoes import request_area_cantoneira, request_resistencia_chapas


class CantoneiraTracionada:
    
    
    def __init__(self):
        '''Larguras efetivas'''
        largura_abas = PegadorParafusada.pega_medida('Insira a largura da aba da cantoneira. ')
        espessura = PegadorParafusada.pega_espessura('Insira a espessura da cantoneira. ')
        self.largura_total_efetiva = CalculadorCantoneiraTracionada.largura_efetiva(largura_abas, 
                                                                                    espessura)
        aba_ate_furo = PegadorParafusada.pega_medida('Insira a largura da aba até o furo (gabarito de furação). ')
        self.largura_efetiva_ate_furos = CalculadorCantoneiraTracionada.largura_efetiva(aba_ate_furo, 
                                                                                        espessura)
        '''Área bruta'''
        self.area_bruta = request_area_cantoneira(largura_abas, espessura)
        
        '''Áreas líquidas'''
        # seção I
        diametro_parafuso = PegadorParafusada.pega_diametro_parafuso()
        medida_furos = CalculadorCantoneiraTracionada.medida_furos(1, diametro_parafuso)
        self.largura_liquida_1 = CalculadorCantoneiraTracionada.largura_liquida(self.largura_total_efetiva, 
                                                                                medida_furos)
        self.area_liquida_1 = CalculadorCantoneiraTracionada.area(self.largura_liquida_1, 
                                                                  espessura)
        
        # seção II
        medida_furos = CalculadorCantoneiraTracionada.medida_furos(2, 
                                                                   diametro_parafuso)
        entre_furos = PegadorParafusada.pega_medida('Insira a medida entre furos. ')
        medida_furos = CalculadorCantoneiraTracionada.medida_furos(2, 
                                                                   diametro_parafuso)
        s = entre_furos / 2
        g = self.largura_efetiva_ate_furos
        ziguezague = CalculadorCantoneiraTracionada.ziguezague(s, g, 1)
        self.largura_liquida_2 = CalculadorCantoneiraTracionada.largura_com_ziguezague(self.largura_total_efetiva,
                                                                                       medida_furos, ziguezague)
        self.area_liquida_2 = CalculadorCantoneiraTracionada.area(self.largura_liquida_2, 
                                                                  espessura)
        
        # seção crítica
        self.secao_critica = self.seleciona_menor_valor(self.area_liquida_1, 
                                                        self.area_liquida_2)
        
        '''Resistência das peças à tração'''
        especificacao_chapa = PegadorParafusada.pega_especificacao_chapa()
        fy, fu = request_resistencia_chapas(especificacao_chapa) if especificacao_chapa != 'Outro' \
                                                 else PegadorParafusada.pega_fy_e_fu('a cantoneira')
        
        # secao bruta
        self.resistencia_bruta = CalculadorCantoneiraTracionada.resistencia_secao_bruta(self.area_bruta, 
                                                                                        fy)
        
        # secao com furos
        self.resistencia_furos = CalculadorCantoneiraTracionada.resistencia_secao_furos(self.secao_critica, 
                                                                                        fu)
        
        # resistencia da peça
        self.resistencia_peca = self.seleciona_menor_valor(self.resistencia_bruta,
                                                           self.resistencia_furos)
        
        '''Maior esforço de cálculo suportado pela peça'''
        self.nd = self.resistencia_peca
        
        '''Esforço nominal'''
        self.esforco_nominal = CalculadorCantoneiraTracionada.esforco_nominal(self.nd)
        
    @staticmethod    
    def seleciona_menor_valor(*valores: float) -> float:
        '''Retorna o menor valor de uma série de valores passados.'''
        
        return min(valores)
    
print(CantoneiraTracionada().__dict__)