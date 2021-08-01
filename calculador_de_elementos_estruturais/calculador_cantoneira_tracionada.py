from calculador_barra_tracionada import CalculadorBarraTracionada

class CalculadorCantoneiraTracionada(CalculadorBarraTracionada):
    
    
    @staticmethod
    def largura_total(largura_abas: float, espessura: float) -> float:
        largura = 2 * largura_abas - espessura
        return largura
    
    @staticmethod
    def gabarito_furacao_efetivo(gabarito_furacao: float, espessura: float) -> float:
        gabarito_efetivo = 2 * gabarito_furacao - espessura
        return gabarito_efetivo