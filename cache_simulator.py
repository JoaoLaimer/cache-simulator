import sys
import struct
import numpy as np

def main():
	if (len(sys.argv) != 7):
		print("Numero de argumentos incorreto. Utilize:")
		print("python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
		exit(1) 
	
	nsets = int(sys.argv[1])
	bsize = int(sys.argv[2])
	assoc = int(sys.argv[3])
	subst = sys.argv[4]
	flagOut = int(sys.argv[5])
	arquivoEntrada = sys.argv[6]
	
	n_bits_offset = int(np.log2(bsize))
	n_bits_indice = int(np.log2(nsets/assoc))
	n_bits_tag = 32 - n_bits_offset - n_bits_indice

	class Cache:

		def __init__(self,nsets,bsize,assoc,subst,flagOut):
			self.nsetspway = nsets/assoc
			self.bsize = bsize
			self.assoc = assoc
			self.subst = subst
			self.flagOut = flagOut
			self.way = [[0] * int(nsets/assoc) for _ in range(assoc)]
			self.arquivoEntrada = arquivoEntrada

			with open(arquivoEntrada, 'rb') as f:
				self.binary_data = f.read()

			self.qntdAdresses = len(self.binary_data) // 4
			self.adressesValues = struct.unpack('>' + 'i' * self.qntdAdresses, self.binary_data)

		def create_cache(self):
			print("Criando cache")
			for i in range(self.assoc):
				for j in range(int(self.nsetspway)):
					self.way[i][j] = Cache_block(self.bsize)
			print("Cache criada")

		def print_atributes(self):
			print("nsets =", int(self.nsetspway), "bsize =", self.bsize, "assoc =", self.assoc)
			print("subst =", self.subst, "flagOut =", self.flagOut)
			for i in range(self.assoc):
				print("way", i)
				print("nsets = ", len(self.way[i]))
				for j in range(int(self.nsetspway)):
					self.way[i][j].print_block()
			print("arquivo =", self.arquivoEntrada)
			print("adresses =", self.adressesValues)

		def read(self):
			
			for i in range(self.qntdAdresses):
				print("Lendo endereço", i)
				tag = self.adressesValues[i] << (n_bits_offset + n_bits_indice)
		

	class Cache_block:
		def __init__(self,bsize):
			self.block = [bsize]	
			self.valid = 0
		def print_block(self):
			print(self.valid,self.block)
			


	C = Cache(nsets,bsize,assoc,subst,flagOut)
	C.create_cache()
	C.print_atributes()

if __name__ == '__main__':
	main()
