import sys
import struct
import numpy as np
import random as rd
from collections import deque


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

	n_bits_indice = int(np.log2(nsets))

	n_bits_tag = 32 - n_bits_offset - n_bits_indice
	if flagOut == 0:
		print("Tamanho offset = ", n_bits_offset, "bits")
		print("Tamanho indice = ", n_bits_indice, "bits")
		print("Tamanho tag = ", n_bits_tag, "bits\n")
	class Cache:

		def __init__(self,nsets,bsize,assoc,subst,flagOut):
			self.nsets = nsets
			self.bsize = bsize
			self.assoc = assoc
			self.subst = subst
			self.flagOut = flagOut
			self.way = [[0] * int(assoc) for _ in range(nsets)]
			#print(self.way)
			self.arquivoEntrada = arquivoEntrada
			if nsets > 1 and assoc == 1:
				self.cacheType = 0
			if nsets > 1 and assoc > 1:
				self.cacheType = 1
			if nsets == 1 and assoc > 1:
				self.cacheType = 2
			
			if (self.subst == 'F' or 'L'):
				self.fila = [deque() for _ in range(nsets)]



			with open(arquivoEntrada, 'rb') as f:
				self.binary_data = f.read()

			self.qntdAdresses = len(self.binary_data) // 4
			self.adressesValues = struct.unpack('>' + 'i' * self.qntdAdresses, self.binary_data)

		def create_cache(self):
			#print("Criando cache")
			for i in range(self.nsets):
				for j in range(int(self.assoc)):
					self.way[i][j] = Cache_block()
			#print("Cache criada")

		def print_atributes(self):
			print("nsets =", int(self.nsets), "bsize =", self.bsize, "assoc =", self.assoc)
			print("subst =", self.subst, "flagOut =", self.flagOut)
			print("Nro de conjuntos:", int(self.nsets))
			print("Tamanho dos conjuntos = ", self.assoc, "blocos")
			print("Tamanho total da Cache = ", self.nsets * self.bsize * self.assoc, "bytes")
			print("Arquivo =", self.arquivoEntrada)
			print("Tipo de Cache :")
			if self.cacheType == 0:
				print("Diretamente mapeada")
			elif self.cacheType == 1:
				print("Conjunto associativa", self.assoc, "- way")
			else:
				print("Totalmente associativa")

			#print("addresses =", self.adressesValues)

		def replace(self, indice, tag, i):
		
			match self.subst:
				
				#Random
				case 'R': 
					r = rd.randrange(0, self.assoc)
					self.way[indice][r].block = tag
					return
					
				#LRU
				case 'L':
					l = self.fila[indice].popleft()
					self.way[indice][l].block = tag
					self.fila[indice].append(l)
					return
					
				#FIFO
				case 'F':
					l = self.fila[indice].popleft()
					self.way[indice][l].block = tag
					self.fila[indice].append(l)
					return
					
				#Random por default
				case _:
					r = rd.randrange(0, self.assoc)
					self.way[indice][r].block = tag
					return
		def is_full(self):
			for i in range(self.nsets):
				for j in range(self.assoc):
					if self.way[i][j].valid == 0:
						return False
			return True

		def direct_mapped(self,indice,tag,missComp,missCap,missConf,hits):
		
			if self.way[indice][0].valid == 0:
				self.way[indice][0].valid = 1
				self.way[indice][0].block = tag
				missComp+=1
				
			else:
				if self.way[indice][0].block != tag:
					self.way[indice][0].block = tag
					if self.is_full():
						missCap+=1
					else:
						missConf+=1

					#print("miss")
				elif self.way[indice][0].block == tag:
					hits+=1
					#print("hit")
			return missComp,missCap,missConf,hits
		
		def associative(self,indice,tag,missComp,missCap,missConf,hits):
			for i in range(self.assoc):
				if self.way[indice][i].valid == 0:
					self.way[indice][i].valid = 1
					self.way[indice][i].block = tag
					if (self.subst == 'F' or 'L'):
						self.fila[indice].append(i)
						
					missComp+=1
					break
				elif self.way[indice][i].block == tag:
					if (self.subst == 'L'):
						self.fila[indice].remove(i)
						self.fila[indice].append(i)
					hits+=1					
					break
				elif (i == (assoc-1)):
					self.replace(indice, tag, i)
					if self.is_full():
						missCap+=1
					else:
						missConf+=1
					break

			return missComp,missCap,missConf,hits

		def read(self):
			hits = 0
			missConf = 0
			missComp = 0
			missCap = 0
			for i in range(self.qntdAdresses):
				tag = self.adressesValues[i] >> (n_bits_offset + n_bits_indice)
				#print("tag = ",tag)
				indice = (self.adressesValues[i] >> n_bits_offset) & ((1 << n_bits_indice)-1)
				#print("indice = ",indice)
				if self.assoc == 1:
					missComp,missCap,missConf,hits = self.direct_mapped(indice,tag,missComp,missCap,missConf,hits)
				else:
					missComp,missCap,missConf,hits = self.associative(indice,tag,missComp,missCap,missConf,hits)

			
			totalAccesses =  missConf+hits+missComp+missCap
			hitRate = hits/totalAccesses
			missRate = (missConf+missComp+missCap)/totalAccesses
			missCompRate = missComp/(missConf+missComp+missCap)
			missCapRate = missCap/(missConf+missComp+missCap)
			missConfRate = missConf/(missConf+missComp+missCap)
			if self.flagOut == 1:
				print("%d" %totalAccesses,"%.4f" %hitRate, "%.4f" %missRate, "%.2f" %missCompRate, "%.2f" %missCapRate, "%.2f" %missConfRate)
				input()
			# total de acessos, taxa de hit, taxa de miss, taxa de miss compulsorio, taxa de miss de capacidade, taxa de miss de conflito
			else:
				print("Total de acessos:", totalAccesses)
				print("Taxa de hit:", hitRate)
				print("Taxa de misses compulsorios:", missCompRate)
				print("Taxa de misses de capacidade:", missCapRate)
				print("Taxa de misses de conflito:", missConfRate)
				input()
		
	class Cache_block:
		def __init__(self):	
			self.valid = 0
			self.block = 0
		def print_block(self):
			print(self.valid)
			
	C = Cache(nsets,bsize,assoc,subst,flagOut)
	C.create_cache()
	if flagOut == 0:
		C.print_atributes()
	C.read()

if __name__ == '__main__':
	main()
