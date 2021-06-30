from sys import argv

with open('versao.txt') as f:
    versao = f.read()
    
versao_grande = int(versao[0])
versao_media = int(versao[2])
versao_pequena = int(versao[4:])

if len(argv) < 2:
    nova_versao = f'{versao_grande}.{versao_media}.{versao_pequena + 1}'
elif argv[1] == 'm':
    nova_versao = f'{versao_grande}.{versao_media + 1}.0'
elif argv[1] == 'g':
    nova_versao = f'{versao_grande + 1}.0.0'

with open('versao.txt', 'w') as f:
    f.write(nova_versao)
    
__init__ = f'''from .menu import MenuPrincipal
#from menu import MenuPrincipal

__version__ = '{nova_versao}'

MenuPrincipal()'''

_setup = f'''from setuptools import setup

setup(name='calculador_de_elementos_estruturais',
    version='{nova_versao}',
    license='Boost Software License',
    author='Doglas Rocha',
    keywords=['Vigas', 'Pilares', 'Ligação Corte Duplo'],
    description=u'Calculador de Elementos Estruturais',
    packages=['calculador_de_elementos_estruturais'],
    install_requires=['pandas'])'''
    
with open('calculador_de_elementos_estruturais/__init__.py', 'w') as f:
    f.write(__init__)
    
with open('setup.py', 'w') as f:
    f.write(_setup)