import sys

def main():
	if (len(sys.argv) != 6):
		print("Numero de argumentos incorreto. Utilize:")
		print("python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
		exit(1)
	
	nsets = int(sys.argv[1])
	bsize = int(sys.argv[2])
	assoc = int(sys.argv[3])
	subst = sys.argv[4]
	flagOut = int(sys.argv[5])
	#arquivoEntrada = sys.argv[6]

	class Cache:

		def __init__(self,nsets,bsize,assoc,subst,flagOut):
			self.nsets = nsets
			self.bsize = bsize
			self.assoc = assoc
			self.subst = subst
			self.flagOut = flagOut
			self.way = []
			#self.arquivoEntrada = arquivoEntrada

		def print_atributes(self):
			print("nsets =", self.nsets)
			print("bsize =", self.bsize)
			print("assoc =", self.assoc)
			print("assoc1 =", len(self.sets))
			print("subst =", self.subst)
			print("flagOut =", self.flagOut)
			for i in range(self.nsets):
				self.sets[i].print_atributes()
			#print("arquivo =", self.arquivoEntrada)

		def create_cache(self):
			print("Criando cache")
			for i in range(self.assoc):
				self.way.append(Cache_way(self.nsets,self.bsize,self.assoc))
			print("Cache criada")

	class Cache_way:
		def __init__(self):
			self.blocks = []	

		
	C = Cache(nsets,bsize,assoc,subst,flagOut)
	C.print_atributes()

if __name__ == '__main__':
	main()
