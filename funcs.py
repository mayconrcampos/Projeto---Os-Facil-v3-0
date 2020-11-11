from datetime import date

class Funcs:
    def valida_valor(self, numero):
        numero = numero.strip()
        if numero.isnumeric():
            return float(numero)
        else:
            c = 0
            for i in numero:
                if i in ",.":
                    c += 1
            if c == 1:
                numero = numero.replace(",", ".")
                return float(numero)
            elif c > 1:
                return False
            else:
                return False

    def data_formatada(self):
        dt = date.today()
        data_form = dt.strftime("%d/%m/%Y")
        return data_form
    

    def concat_produto(self, prod, desc):
        return f"{prod} - {desc}"

    
    def desconcat_produto(self, prod):
        produto = ""
        pos = 0
        for letra in prod:
            if letra not in "-":
                produto += letra
                pos += 1
            else:
                break
        
        prod2 = ""
        for i in range(pos + 2, len(prod)):
            prod2 += prod[i]
        
        return produto[1:-2], prod2

   
    
    def sub_total(self, qtde, valor):
        qtde = int(qtde)
        valor = float(valor)
        return qtde * valor
    