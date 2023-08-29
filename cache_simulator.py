import sys
import struct
import numpy as np
import random as rd
from collections import deque


def main():
	#if (len(sys.argv) != 7):
	#	print("Numero de argumentos incorreto. Utilize:")
	#	print("python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
	#	exit(1) 
	
	nsets = 4 #int(sys.argv[1])
	bsize = 4#int(sys.argv[2])
	assoc = 2#int(sys.argv[3])
	subst = 'L'#sys.argv[4]
	flagOut = 1#int(sys.argv[5])
	arquivoEntrada = "./Endereços/bin_100.bin"#sys.argv[6]
	
	n_bits_offset = int(np.log2(bsize))
	print("offset = ",n_bits_offset)
	n_bits_indice = int(np.log2(nsets))
	print("indice = ",n_bits_indice)
	n_bits_tag = 32 - n_bits_offset - n_bits_indice
	print("tag = ",n_bits_tag)

	class Cache:

		def __init__(self,nsets,bsize,assoc,subst,flagOut):
			self.nsets = nsets
			self.bsize = bsize
			self.assoc = assoc
			self.subst = subst
			self.flagOut = flagOut
			self.way = [[0] * int(assoc) for _ in range(nsets)]
			print(self.way)
			self.arquivoEntrada = arquivoEntrada
			
			if (self.subst == 'F' or 'L'):
				self.fila = [deque() for _ in range(nsets)]



			with open(arquivoEntrada, 'rb') as f:
				self.binary_data = f.read()

			self.qntdAdresses = len(self.binary_data) // 4
			self.adressesValues = struct.unpack('>' + 'i' * self.qntdAdresses, self.binary_data)

		def create_cache(self):
			print("Criando cache")
			for i in range(self.nsets):
				for j in range(int(self.assoc)):
					self.way[i][j] = Cache_block()
			print("Cache criada")

		def print_atributes(self):
			print("nsets =", int(self.nsets), "bsize =", self.bsize, "assoc =", self.assoc)
			print("subst =", self.subst, "flagOut =", self.flagOut)
			for i in range(self.nsets):
				print("way = ", i)
				print("nsets = ", len(self.way[i]))
			print("arquivo =", self.arquivoEntrada)
			#print("addresses =", self.adressesValues)

		def replace(self, indice, tag, i):
		
			match self.subst:
				
				#Random
				case 'R': 
					r = rd.randrange(0, self.nsets)
					self.way[indice][r] = tag
					return
					
				#LRU
				case 'L':
					l = self.fila[indice].popleft()
					self.way[indice][l] = tag
					self.fila[indice].append(i)
					return
					
				#FIFO
				case 'F':
					self.way[indice][self.fila[indice].popleft()] = tag
					self.fila[indice].append(i)
					return
					
				#Random por default
				case _:
					r = rd.randint(0, self.nsets-1)
					self.way[indice][r] = tag
					return

		def direct_mapped(self,indice,tag,miss,hits):
		
			if self.way[indice][0].valid == 0:
				self.way[indice][0].valid = 1
				self.way[indice][0].block = tag
				miss+=1
				print("miss comp")
			else:
				if self.way[indice][0].block != tag:
					self.way[indice][0].block = tag
					miss+=1
					print("miss")
				elif self.way[indice][0].block == tag:
					hits+=1
					print("hit")
			return miss,hits
		
		def associative(self,indice,tag,miss,hits):
			for i in range(self.assoc):
				if self.way[indice][i].valid == 0:
					self.way[indice][i].valid = 1
					self.way[indice][i].block = tag
					if (self.subst == 'F' or 'L'):
						self.fila[indice].append(i)
						
					miss+=1
					break
				elif self.way[indice][i].block == tag:
					if (self.subst == 'L'):
						self.fila[indice].remove(i)
						self.fila[indice].append(i)
					hits+=1					
					break
				elif (i == (assoc-1)):
					self.replace(self, indice, tag, i)
					miss+=1
					break

			return miss,hits

		def read(self):
			miss = 0
			hits = 0
			for i in range(self.qntdAdresses):
				tag = self.adressesValues[i] >> (n_bits_offset + n_bits_indice)
				print("tag = ",tag)
				indice = (self.adressesValues[i] >> n_bits_offset) & ((1 << n_bits_indice)-1)
				print("indice = ",indice)
				if self.assoc == 1:
					miss,hits = self.direct_mapped(indice,tag,miss,hits)
				else:
					miss,hits = self.associative(indice,tag,miss,hits)
			print(" miss=",miss," hits=",hits," total=",miss+hits," taxa=",(hits/(miss+hits))*100,"%")


		
	class Cache_block:
		def __init__(self):	
			self.valid = 0
			self.block = 0
		def print_block(self):
			print(self.valid)
			


	C = Cache(nsets,bsize,assoc,subst,flagOut)
	C.create_cache()
	C.print_atributes()
	C.read()


if __name__ == '__main__':
	main()
