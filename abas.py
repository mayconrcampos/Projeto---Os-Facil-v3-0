import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from db import Db
from funcs import Funcs

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image

#import webbrowser


    ################################
    ####### Janela Principal #######
    ################################

class Aba_01:
    def botoes_aba_01(self):
        self.btn_cad_clientes = self.builder.get_object("btn_cadastrar_clientes")
        self.btn_cad_produtos = self.builder.get_object("btn_cadastrar_produtos")
        self.btn_os = self.builder.get_object("btn_os")
        self.btn_historico = self.builder.get_object("btn_historico")
        self.btn_sobre = self.builder.get_object("btn_sobre")
        self.btn_sair = self.builder.get_object("btn_sair")
    
    def liga_stack(self):
        self.stack: Gtk.Stack = self.builder.get_object("stack")

    def liga_botoes_aba_01(self):
        self.btn_sair.connect("clicked", self.on_clicked_btn_sair)
        self.btn_cad_clientes.connect("clicked", self.on_clicked_btn_cadastrar_clientes)
        self.btn_cad_produtos.connect("clicked", self.on_clicked_btn_cadastrar_produtos)
        self.btn_os.connect("clicked", self.on_clicked_btn_os)
        self.btn_historico.connect("clicked", self.on_clicked_btn_historico)
        self.btn_sobre.connect("clicked", self.on_clicked_btn_sobre)

        

    
    def on_clicked_btn_sair(self, btn):
        Gtk.main_quit()
    
    def on_clicked_btn_cadastrar_clientes(self, btn):
        self.stack.set_visible_child_name("page1")
    
    def on_clicked_btn_cadastrar_produtos(self, btn):
        self.stack.set_visible_child_name("page2")
    
    def on_clicked_btn_os(self, btn):
        self.stack.set_visible_child_name("page3")
    
    def on_clicked_btn_historico(self, btn):
        self.stack.set_visible_child_name("page5")
        self.mostrar_tview_historico_os()
    
    def on_clicked_btn_sobre(self, btn):
        self.stack.set_visible_child_name("page6")

    #####################################
    ####### Cadastro de Clientes ########
    #####################################

class Aba_02:
    def botoes_aba_02(self):
        self.btn_adicionar_cliente = self.builder.get_object("btn_adicionar_cliente")
        self.btn_alterar_cliente = self.builder.get_object("btn_alterar_cliente")
        self.btn_excluir_cliente = self.builder.get_object("btn_excluir_cliente")
        self.btn_limpar_clientes =self.builder.get_object("btn_limpar_clientes")
        self.btn_voltar_aba_02 = self.builder.get_object("btn_voltar_aba_02")
        self.tview_clientes = self.builder.get_object("liststore_tview_clientes")
        self.seleciona_clientes = self.builder.get_object("seleciona_clientes")

        self.cmb_tipo_cliente = self.builder.get_object("entra_cmb_cliente")
        self.entra_nome_cliente = self.builder.get_object("entra_nome_cliente")
        self.entra_contato_cliente = self.builder.get_object("entra_contato_cliente")
        self.entra_id_cliente = self.builder.get_object("entra_id_cliente")

    
    def liga_botoes_aba_02(self):
        self.btn_adicionar_cliente.connect("clicked", self.on_clicked_btn_adicionar_cliente)
        self.btn_alterar_cliente.connect("clicked", self.on_clicked_btn_alterar_cliente)
        self.btn_excluir_cliente.connect("clicked", self.on_clicked_btn_excluir_cliente)
        self.btn_limpar_clientes.connect("clicked", self.on_clicked_btn_limpar_clientes)
        self.btn_voltar_aba_02.connect("clicked", self.on_clicked_btn_voltar_aba_02)
        self.seleciona_clientes.connect("changed", self.cliente_selecionado)
    
    def on_clicked_btn_adicionar_cliente(self, btn):
        tipo = self.cmb_tipo_cliente.get_text()
        nome = self.entra_nome_cliente.get_text()
        contato = self.entra_contato_cliente.get_text()
        if tipo and nome and contato:
            self.conecta_db()
            self.cursor.execute("""INSERT INTO clientes (tipo, nome, contato) VALUES (?,?,?)""",(tipo, nome, contato))
            self.conn.commit()
            self.desconecta_db()

            self.combo_os.append_text(nome)
            self.cmb_tipo_cliente.set_text("")
            self.entra_id_cliente.set_text("")
            self.entra_nome_cliente.set_text("")
            self.entra_contato_cliente.set_text("")

            self.tview_clientes.clear()
            self.mostrar_tview_clientes()
            
            
            
        else:
            self.mensagem("Você precisa preencher todos os campos para Adicionar")
    
    def on_clicked_btn_alterar_cliente(self, btn):
        id = self.entra_id_cliente.get_text()
        tipo = self.cmb_tipo_cliente.get_text()
        nome = self.entra_nome_cliente.get_text()
        contato = self.entra_contato_cliente.get_text()
        if id:
            self.conecta_db()
            self.cursor.execute("""UPDATE clientes SET tipo=?, nome=?, contato=? WHERE id=?""",(tipo, nome, contato, id))
            self.conn.commit()
            self.desconecta_db()

            self.limpar_clientes()

            self.tview_clientes.clear()
            self.mostrar_tview_clientes()
        else:
            self.mensagem("Você precisa selecionar um cliente para Alterar.")

    
    def on_clicked_btn_excluir_cliente(self, btn):
        id = self.entra_id_cliente.get_text()
        if id:
            self.conecta_db()
            self.cursor.execute("""DELETE FROM clientes WHERE id=?""",(id,))
            self.conn.commit()
            self.desconecta_db()

            self.tview_clientes.clear()
            self.mostrar_tview_clientes()
        else:
            self.mensagem("Você precisa selecionar um cliente para Excluir.")
    
    def on_clicked_btn_limpar_clientes(self, btn):
        self.limpar_clientes()


    def on_clicked_btn_voltar_aba_02(self, btn):
        self.stack.set_visible_child_name("page0")
    
    def mostrar_tview_clientes(self):
        self.conecta_db()
        lista = self.cursor.execute("""SELECT id, tipo, nome, contato FROM clientes ORDER BY nome;""")
        for linha in lista:
            self.tview_clientes.append(linha)
        self.desconecta_db()
    
    def cliente_selecionado(self, selecionado):
        modelo, linha = selecionado.get_selected()
        if linha:
            self.cmb_tipo_cliente.set_text(modelo[linha][1])
            self.entra_id_cliente.set_text(str(modelo[linha][0]))
            self.entra_nome_cliente.set_text(modelo[linha][2])
            self.entra_contato_cliente.set_text(modelo[linha][3])
    
    def limpar_clientes(self):
        self.cmb_tipo_cliente.set_text("")
        self.entra_id_cliente.set_text("")
        self.entra_nome_cliente.set_text("")
        self.entra_contato_cliente.set_text("")


    ##################################
    ###### Cadastro de Produtos ######
    ##################################

class Aba_03:
    def botoes_aba_03(self):
        self.entra_tipo_produto = self.builder.get_object("entra_tipo_produto")
        self.entra_descricao_produto = self.builder.get_object("entra_descricao_produto")
        self.entra_codigo_produto = self.builder.get_object("entra_codigo_produto")
        self.entra_valor_produto = self.builder.get_object("entra_valor_produto")
        self.entra_id_produto = self.builder.get_object("entra_id_produto")
        self.seleciona_produtos = self.builder.get_object("seleciona_produtos")
        

        self.btn_adicionar_produto = self.builder.get_object("btn_adicionar_produto")
        self.btn_alterar_produto = self.builder.get_object("btn_alterar_produto")
        self.btn_excluir_produto = self.builder.get_object("btn_excluir_produto")
        self.btn_limpar_produto = self.builder.get_object("btn_limpar_produtos")
        self.btn_voltar_aba_03 = self.builder.get_object("btn_voltar_aba_03")
        self.tview_produtos = self.builder.get_object("liststore_tview_produtos")
    
    def liga_botoes_aba_03(self):
        self.btn_adicionar_produto.connect("clicked", self.on_btn_adicionar_produto_clicked)
        self.btn_alterar_produto.connect("clicked", self.on_btn_alterar_produto_clicked)
        self.btn_excluir_produto.connect("clicked", self.on_btn_excluir_produto_clicked)
        self.btn_limpar_produto.connect("clicked", self.on_btn_limpar_produtos_clicked)
        self.btn_voltar_aba_03.connect("clicked", self.on_btn_voltar_aba_03_clicked)
        self.seleciona_produtos.connect("changed", self.produto_selecionado)
    
    
    def on_btn_adicionar_produto_clicked(self, btn):
        tipo = self.entra_tipo_produto.get_text()
        descricao = self.entra_descricao_produto.get_text()
        codigo = self.entra_codigo_produto.get_text()
        valor = self.valida_valor(self.entra_valor_produto.get_text())
        
        if tipo and descricao and codigo and valor:
            self.conecta_db()
            lista = self.cursor.execute("""SELECT tipo, descricao, codigo, valor FROM produtos;""")

            flag = 0
            for linha in lista:
                if descricao == linha[1] or codigo == linha[2]:
                    flag += 1
            
            if not flag:
                self.cursor.execute("""INSERT INTO produtos (tipo, descricao, codigo, valor) VALUES (?,?,?,?)""", (tipo, descricao, codigo, float(valor)))
            else:
                self.mensagem("ERRO! Este Produto/Serviço já existe na lista.")


            self.conn.commit()
            self.desconecta_db()

            self.limpar_produtos()

            self.tview_produtos.clear()
            self.mostrar_tview_produtos()
    
    def on_btn_alterar_produto_clicked(self, btn):
        id = self.entra_id_produto.get_text()
        tipo = self.entra_tipo_produto.get_text()
        descricao = self.entra_descricao_produto.get_text()
        codigo = self.entra_codigo_produto.get_text()
        valor = self.entra_valor_produto.get_text()
        if id:
            self.conecta_db()
            self.cursor.execute("""UPDATE produtos SET tipo=?, descricao=?, codigo=?, valor=? WHERE id=?""",(tipo, descricao, codigo, valor, id))
            self.conn.commit()
            self.desconecta_db()

            self.limpar_produtos()
            self.tview_produtos.clear()
            self.mostrar_tview_produtos()



    def on_btn_excluir_produto_clicked(self, btn):
        id = self.entra_id_produto.get_text()
        if id:
            self.conecta_db()
            self.cursor.execute("""DELETE FROM produtos WHERE id=?""",(id,))
            self.conn.commit()
            self.desconecta_db()

            self.tview_produtos.clear()
            self.mostrar_tview_produtos()
    
    def on_btn_limpar_produtos_clicked(self, btn):
        self.limpar_produtos()
    
    def on_btn_voltar_aba_03_clicked(self, btn):
        self.stack.set_visible_child_name("page0")
    

    def mostrar_tview_produtos(self):
        self.conecta_db()
        lista = self.cursor.execute("""SELECT id, tipo, descricao, codigo, valor FROM produtos ORDER BY codigo;""")
        for linha in lista:
            self.tview_produtos.append(linha)
        self.desconecta_db()
    
    def produto_selecionado(self, selecionado):
        modelo, linha = selecionado.get_selected()
        if linha:
            self.entra_id_produto.set_text(str(modelo[linha][0]))
            self.entra_tipo_produto.set_text(modelo[linha][1])
            self.entra_descricao_produto.set_text(modelo[linha][2])
            self.entra_codigo_produto.set_text(modelo[linha][3])
            self.entra_valor_produto.set_text(str(modelo[linha][4]))
    
    def limpar_produtos(self):
        self.entra_id_produto.set_text("")
        self.entra_tipo_produto.set_text("")
        self.entra_descricao_produto.set_text("")
        self.entra_codigo_produto.set_text("")
        self.entra_valor_produto.set_text("")

    #################################
    ####### Janela Cadastro OS ######
    #################################


class Aba_04:
    def botoes_aba_04(self):
        self.entra_cliente_os = self.builder.get_object("entra_cliente_os")
        self.combo_os = self.builder.get_object("combo_lista_clientes")
        

        self.entra_numero_os = self.builder.get_object("entra_numero_os")
        self.entra_data_os = self.builder.get_object("entra_data_os")
        self.entra_entrada_os = self.builder.get_object("entra_entrada_os")
        self.entra_id_os = self.builder.get_object("entra_id_os")
        self.btn_add_entrada_os = self.builder.get_object("btn_add_entrada_os")
        self.btn_adiciona_os = self.builder.get_object("btn_adiciona_os")
        self.btn_visualiza_produtos_os = self.builder.get_object("btn_visualiza_produtos_os")
        self.btn_dar_baixa_os = self.builder.get_object("btn_dar_baixa_os")
        self.btn_salvar_pdf_os = self.builder.get_object("btn_salvar_pdf_os")
        self.btn_limpar_os = self.builder.get_object("btn_limpar_os")
        self.btn_voltar_aba_04 = self.builder.get_object("btn_voltar_aba_04")
        self.entra_pendente_os = self.builder.get_object("entra_pendente_os")
        self.entra_pago_os = self.builder.get_object("entra_pago_os")
        self.entra_total_os = self.builder.get_object("entra_total_os")
        self.tview_os = self.builder.get_object("liststore_tview_os")
        self.seleciona_os = self.builder.get_object("seleciona_os")
        
        data = self.data_formatada()
        self.entra_data_os.set_text(data)


    
    def liga_botoes_aba_04(self):
        self.btn_add_entrada_os.connect("clicked",self.on_btn_add_entrada_os_clicked)
        self.btn_adiciona_os.connect("clicked",self.on_btn_adiciona_os_clicked)
        self.btn_visualiza_produtos_os.connect("clicked", self.btn_visualiza_produtos_os_clicked)
        self.btn_dar_baixa_os.connect("clicked", self.btn_dar_baixa_os_clicked)
        self.btn_salvar_pdf_os.connect("clicked", self.btn_salvar_pdf_os_clicked)
        self.btn_limpar_os.connect("clicked", self.btn_limpar_os_clicked)
        self.btn_voltar_aba_04.connect("clicked", self.btn_voltar_aba_04_clicked)
        self.combo_os.connect("changed", self.on_combo)
        self.seleciona_os.connect("changed", self.os_selecionado)


    
    def on_combo(self, widget):
        cliente = widget.get_active_text()
        self.entra_cliente_os.set_text(cliente)
        
    def on_btn_add_entrada_os_clicked(self, btn):
        os = self.entra_numero_os.get_text()

        entrada = self.valida_valor(self.entra_entrada_os.get_text())
        if os and entrada:
            self.conecta_db()
            lista = self.cursor.execute("""SELECT os, total FROM os;""")
            total = 0
            for linha in lista:
                if os == linha[0]:
                    total = linha[1]
            
            if float(entrada) <= total:
                self.cursor.execute("""UPDATE os SET entrada=? WHERE os=?""",(float(entrada), os))
                self.conn.commit()
                self.desconecta_db()
                self.tview_os.clear()
                self.mostrar_tview_os()
            else:
                self.desconecta_db()
                self.mensagem("ERRO!\nVocê precisa definir uma entrada menor ou igual ao total da OS.")        


    def on_btn_adiciona_os_clicked(self, btn):
        cliente = self.combo_os.get_active_text()
  
        if cliente:
            os = self.gera_os(cliente)
            data = self.data_formatada()
            self.conecta_db()
            self.cursor.execute("""INSERT INTO os (cliente, os, data, entrada, total, status) VALUES (?,?,?,?,?,?)""",(cliente, os, data, 0.0, 0.0, "Ativo"))
            self.conn.commit()
            self.desconecta_db()

            self.limpa_os()
            self.tview_os.clear()
            self.mostrar_tview_os()
    

    def btn_visualiza_produtos_os_clicked(self, btn):
        os = self.entra_numero_os.get_text()
        cliente = self.entra_cliente_os.get_text()
        data = self.entra_data_os.get_text()
        if os and cliente and data:
            self.entra_os_cp.set_text(os)
            self.entra_cliente_cp.set_text(cliente)
            self.entra_data_cp.set_text(data)
            self.stack.set_visible_child_name("page4")
            self.mostrar_tview_cp_baixo()            

    
    def btn_dar_baixa_os_clicked(self, btn):
        id = self.entra_id_os.get_text()
        if id:
            self.conecta_db()
            lista = self.cursor.execute("""SELECT id, entrada, total FROM os;""")
            entrada = 0
            total = 0
            for linha in lista:
                if linha[0] == int(id):
                    entrada = linha[1]
                    total = linha[2]

            if not total:
                self.mensagem("Você precisa fazer:\n1 - Inserir Itens.\n2 - Definir uma entrada.\n3 - Dar Baixa.")
            else:
                if total == entrada:
                    self.cursor.execute("""UPDATE os SET status=? WHERE id=?""",("Quitado", int(id)))
                    self.conn.commit()
                    self.desconecta_db()
                    self.tview_os.clear()
                    self.mostrar_tview_os()

                elif total > entrada:
                    self.mensagem("Você precisa quitar esta OS definindo a Entrada.")

            
    def salvar_pdf(self):
        self.os = self.entra_numero_os.get_text()
        self.nome_pdf = f"OS/OS_{self.os}.pdf"
        #self.webbrowser.open(self.nome_pdf)

    def btn_salvar_pdf_os_clicked(self, btn):
        self.os = self.entra_numero_os.get_text()
        self.cliente = self.entra_cliente_os.get_text()
        self.data = self.entra_data_os.get_text()

        self.conecta_db()
        lista = self.cursor.execute("""SELECT os, entrada, total FROM os;""")
        total = 0
        entrada = 0
        for linha in lista:
            if self.os == linha[0]:
                total = linha[2]
                entrada = linha[1]

        self.desconecta_db()

        if self.os and total:
            self.nome_pdf = f"OS/OS_{self.os}.pdf"
            self.c = canvas.Canvas(self.nome_pdf)

            self.c.setFont("Helvetica", 18)
            self.c.drawString(80, 800, "OS Fácil v3.0 - AM Sublimação - Ordem de Serviço")
            self.c.drawString(50, 785, "--------------------------------------------------------------------------------")
            self.c.setFont("Helvetica", 14)
            self.c.drawString(50, 770, f"Data : {self.data} | Cliente: {self.cliente:<40}     | OS: {self.os}")
            self.c.setFont("Helvetica", 18)
            self.c.drawString(50, 755, "--------------------------------------------------------------------------------")
            self.c.setFont("Helvetica", 11)
            self.c.drawString(20, 740, "Item Nº  | Preço Uni  | Qtde UNI | Subtotal    | Descrição do Produto")
            self.comprimento = 730
            self.c.drawString(20, self.comprimento, "-----------------------------------------------------------------------------------------------------------------------------------------------------")
            
            self.conecta_db()
            lista1 = self.cursor.execute("""SELECT os, valor_uni, descricao, qtde, sub_total FROM cp ORDER BY descricao;""")
            
            item = 1
            conta_itens = 0
            
            for i in lista1:
                if i[0] == self.os:
                    self.comprimento -= 13
                    self.c.drawString(20, self.comprimento, f"Item: {item:0>2} | R$ {i[1]:0^6.2f} | Qtde: {i[3]:0>2}   | R$: {i[-1]:0>7.2f} | {i[2]:<50}")
                    conta_itens += i[3]
                    item += 1

            pendente = total - entrada

            self.comprimento -= 15
            self.c.drawString(20, self.comprimento, "---------------------------------------------------------------------------------------------------------------------------------------------------")
            self.comprimento -= 15
            self.c.drawString(20, self.comprimento, f"Total: {conta_itens:0>3} Itens | Total Pedido R$: {total:.2f} | Entrada R$: {entrada:.2f} | Falta Pagar R$: {pendente:.2f}")
            self.comprimento -= 15
            self.c.drawString(20, self.comprimento, "---------------------------------------------------------------------------------------------------------------------------------------------------")
            self.desconecta_db()


            self.c.showPage()
            self.c.save()

            self.salvar_pdf()
        
        else:
            self.mensagem("ERRO! Você precisa selecionar uma OS com produtos para Gerar o PDF.")
    
    def btn_limpar_os_clicked(self, btn):
        self.limpa_os()
    
    def btn_voltar_aba_04_clicked(self, btn):
        self.stack.set_visible_child_name("page0")
    
    
    def lista_clientes(self):
        self.conecta_db()
        lista = self.cursor.execute("""SELECT nome FROM clientes ORDER BY nome;""")
        for linha in lista:
            self.combo_os.append_text(linha[0])

        self.desconecta_db()
    
    def limpa_os(self):
        self.entra_entrada_os.set_text("")
        self.entra_id_os.set_text("")
    
    def gera_os(self, nome):
        self.conecta_db()
        lista = self.cursor.execute("""SELECT id, cliente FROM os;""")
        numero = []
        maisum = 0
        for linha in lista:    
            numero.append(linha[0])

        maisum = len(numero) + 1
        self.desconecta_db()
        data = self.data_formatada()
        return f"{data[8:]}-{maisum}"
    
    def mostrar_tview_os(self):
        self.conecta_db()
        lista = self.cursor.execute("""SELECT id, cliente, os, data, entrada, total, status FROM os;""")
        total = 0
        entrada = 0
        for linha in lista:
            if linha[6] == "Ativo":
                total += linha[5]
                entrada += linha[4]
                self.tview_os.append(linha)
        
        pendente = total - entrada
        self.entra_total_os.set_text(str(total))
        self.entra_pago_os.set_text(str(entrada))
        self.entra_pendente_os.set_text(str(pendente))
        self.desconecta_db()


    def os_selecionado(self, selecionado):
        modelo, linha = selecionado.get_selected()
        if linha:
            self.entra_cliente_os.set_text(str(modelo[linha][1]))
            self.entra_numero_os.set_text(modelo[linha][2])
            self.entra_data_os.set_text(modelo[linha][3])
            self.entra_entrada_os.set_text(str(modelo[linha][4]))
            self.entra_id_os.set_text(str(modelo[linha][0]))

    
    #############################
    #Janela Cadastro de Produtos#
    #############################

class Aba_05:
    def botoes_aba_05(self):
        self.entra_os_cp = self.builder.get_object("entra_os_cp")
        self.entra_cliente_cp = self.builder.get_object("entra_cliente_cp")
        self.entra_data_cp = self.builder.get_object("entra_data_cp")
        self.entra_qtde_cp = self.builder.get_object("entra_qtde_cp")
        self.entra_produto_cp = self.builder.get_object("entra_produto_cp")
        self.entra_descricao_cp = self.builder.get_object("entra_descricao_cp")
        self.entra_valor_cp = self.builder.get_object("entra_valor_cp")
        self.entra_id_cp = self.builder.get_object("entra_id_cp")

        self.btn_add_produto_cp = self.builder.get_object("btn_add_produto_cp")
        self.btn_alterar_cp = self.builder.get_object("btn_alterar_cp")
        self.btn_excluir_cp = self.builder.get_object("btn_excluir_cp")
        self.btn_limpar_cp = self.builder.get_object("btn_limpar_cp")
        self.btn_voltar_cp = self.builder.get_object("btn_voltar_cp")

        self.entra_pendente_cp = self.builder.get_object("entra_pendente_cp")
        self.entra_pago_cp = self.builder.get_object("entra_pago_cp")
        self.entra_total_cp = self.builder.get_object("entra_total_cp")

        # Treeview de cima
        self.seleciona_cp = self.builder.get_object("seleciona_cp")
        self.liststore_tview_produtos = self.builder.get_object("liststore_tview_produtos")

        # Treeview de baixo
        self.seleciona_prod_cp = self.builder.get_object("seleciona_prod_cp")
        self.liststore_tview_cp = self.builder.get_object("liststore_tview_cp")

    

    def liga_botoes_aba_05(self):
        self.btn_add_produto_cp.connect("clicked", self.on_clicked_btn_add_produto_cp)
        self.btn_alterar_cp.connect("clicked", self.on_clicked_btn_alterar_cp)
        self.btn_excluir_cp.connect("clicked", self.on_clicked_btn_excluir_cp)
        self.btn_limpar_cp.connect("clicked", self.on_clicked_btn_limpar_cp)
        self.btn_voltar_cp.connect("clicked", self.on_clicked_btn_voltar_cp)

        # Tview de cima
        self.seleciona_cp.connect("changed", self.cp_selecionado_cima)

        # Tview de Baixo
        self.seleciona_prod_cp.connect("changed", self.cp_selecionado_baixo)


    
    def variaveis_aba_05(self):
        self.os = self.entra_os_cp.get_text()
        self.cliente = self.entra_cliente_cp.get_text()
        self.data = self.entra_data_cp.get_text()


    def on_clicked_btn_add_produto_cp(self, btn):
        os = self.entra_os_cp.get_text()
        qtde = self.entra_qtde_cp.get_text()
        prod = self.entra_produto_cp.get_text()
        desc = self.entra_descricao_cp.get_text()
        descricao = self.concat_produto(prod, desc)
        valor = self.entra_valor_cp.get_text()
        sub_total = self.sub_total(qtde, valor)
        if os and qtde and descricao and valor:
            self.conecta_db()
            self.cursor.execute("""INSERT INTO cp (os, valor_uni, descricao, qtde, sub_total) VALUES (?,?,?,?,?)""",(os, valor, descricao, qtde, sub_total))
            self.conn.commit()
            self.desconecta_db()
            self.entra_qtde_cp.set_text("")
            #self.entra_produto_cp.set_text("")
            self.entra_descricao_cp.set_text("")
            #self.entra_valor_cp.set_text("")
            self.entra_id_cp.set_text("")
            self.liststore_tview_cp.clear()
            self.mostrar_tview_cp_baixo()

    
    def on_clicked_btn_alterar_cp(self, btn):
        ide = self.entra_id_cp.get_text()
        qtde = self.entra_qtde_cp.get_text()
        prod = self.entra_produto_cp.get_text()
        desc = self.entra_descricao_cp.get_text()
        descricao = self.concat_produto(prod, desc)
        vlr_uni = self.entra_valor_cp.get_text()
        if ide and descricao and qtde:
            self.conecta_db()
            
            sub_total = int(qtde) * float(vlr_uni)
        
            self.cursor.execute("""UPDATE cp SET valor_uni=?, qtde=?, descricao=?, sub_total=? WHERE id=?""",(vlr_uni ,int(qtde), descricao, sub_total, int(ide)))
            self.conn.commit()
            self.desconecta_db()
            
            self.liststore_tview_cp.clear()
            self.mostrar_tview_cp_baixo()
            
            self.tview_os.clear()
            self.mostrar_tview_os()

            self.entra_qtde_cp.set_text("")
            self.entra_produto_cp.set_text("")
            self.entra_descricao_cp.set_text("")
            self.entra_valor_cp.set_text("")
            self.entra_id_cp.set_text("")
        else:
            self.mensagem("ERRO! Você precisa selecionar um item para Alterar.")
    
    def on_clicked_btn_excluir_cp(self, btn):
        ide = self.entra_id_cp.get_text()
        if ide:
            self.conecta_db()
            self.cursor.execute("""DELETE FROM cp WHERE id=?""",(int(ide),))
            self.conn.commit()
            self.desconecta_db()

            self.tview_os.clear()
            self.mostrar_tview_os()

            self.liststore_tview_cp.clear()
            self.mostrar_tview_cp_baixo()

            self.entra_qtde_cp.set_text("")
            self.entra_produto_cp.set_text("")
            self.entra_descricao_cp.set_text("")
            self.entra_valor_cp.set_text("")
            self.entra_id_cp.set_text("")
        else:
            self.mensagem("ERRO! Você precisa selecionar um item para Excluir.")
    
    def on_clicked_btn_limpar_cp(self, btn):
        self.entra_qtde_cp.set_text("")
        self.entra_produto_cp.set_text("")
        self.entra_descricao_cp.set_text("")
        self.entra_valor_cp.set_text("")
        self.entra_id_cp.set_text("")
    
    def on_clicked_btn_voltar_cp(self, btn):
        self.stack.set_visible_child_name("page3")


    def cp_selecionado_cima(self, selecionado):
        modelo, linha = selecionado.get_selected()
        if linha:
            self.entra_produto_cp.set_text(modelo[linha][2])
            self.entra_valor_cp.set_text(str(modelo[linha][4]))
        

    def mostrar_tview_cp_baixo(self):
        self.liststore_tview_cp.clear()
        os = self.entra_os_cp.get_text()
        if os:
            self.conecta_db()
            lista = self.cursor.execute("""SELECT id, os, valor_uni, descricao, qtde, sub_total FROM cp ORDER BY descricao;""")
            total = 0
            for linha in lista:
                if linha[1] == os:
                    total += linha[5]                    
                    self.liststore_tview_cp.append(linha)
            
            lista1 = self.cursor.execute("""SELECT os, entrada FROM os;""")
            pago = 0
            for linha1 in lista1:
                if os == linha1[0]:
                    pago = linha1[1]
                

            pendente = total - pago
            self.cursor.execute("""UPDATE os SET total=? WHERE os=?""",(total, os))
            self.conn.commit()
            
            self.entra_pendente_cp.set_text(str(pendente))
            self.entra_pago_cp.set_text(str(pago))
            self.entra_total_cp.set_text(str(total))

            self.desconecta_db()

            self.tview_os.clear()
            self.mostrar_tview_os()
    

    def cp_selecionado_baixo(self, selecionado):
        modelo, linha = selecionado.get_selected()
        if linha:
            prod, desc = self.desconcat_produto(modelo[linha][3])
            self.entra_produto_cp.set_text(prod)
            self.entra_descricao_cp.set_text(desc)
            self.entra_qtde_cp.set_text(str(modelo[linha][4]))
            self.entra_valor_cp.set_text(str(modelo[linha][2]))
            self.entra_id_cp.set_text(str(modelo[linha][0]))
    
    ##################################
    ######## Janela Histórico ########
    ################################## 

class Aba_06:
    def botoes_aba_06(self):
        self.seleciona_historico_os = self.builder.get_object("seleciona_historico_os")
        self.liststore_historico_os = self.builder.get_object("liststore_historico_os")

        self.seleciona_historico_produtos = self.builder.get_object("seleciona_historico_produtos")
        self.liststore_historico_produtos = self.builder.get_object("liststore_historico_produtos")

        self.entra_os_his = self.builder.get_object("entra_os_his")
        self.entra_cliente_his = self.builder.get_object("entra_cliente_his")
        
        self.btn_visualizar_his = self.builder.get_object("btn_visualizar_his")
        self.btn_limpar_his = self.builder.get_object("btn_limpar_his")
        self.btn_voltar_his = self.builder.get_object("btn_voltar_his")

        self.entra_pendente_his = self.builder.get_object("entra_pendente_his")
        self.entra_pago_his = self.builder.get_object("entra_pago_his")
        self.entra_total_his = self.builder.get_object("entra_total_his")

    
    def liga_botoes_aba_06(self):
        self.btn_visualizar_his.connect("clicked", self.on_clicked_btn_visualizar_his)
        self.btn_limpar_his.connect("clicked", self.on_clicked_btn_limpar_his)
        self.btn_voltar_his.connect("clicked", self.on_clicked_btn_voltar_his)

        self.seleciona_historico_os.connect("changed", self.historico_os_selecionado)


    def on_clicked_btn_visualizar_his(self, btn):
        os = self.entra_os_his.get_text()
        self.liststore_historico_produtos.clear()
        if os:
            self.conecta_db()
            lista = self.cursor.execute("""SELECT id, os, valor_uni, descricao, qtde, sub_total FROM cp ORDER BY descricao;""")
            for linha in lista:
                if os == linha[1]:
                    self.liststore_historico_produtos.append(linha)
            self.desconecta_db()
    
    def on_clicked_btn_limpar_his(self, btn):
        self.entra_cliente_his.set_text("")
        self.entra_os_his.set_text("")
    
    def on_clicked_btn_voltar_his(self, btn):
        self.stack.set_visible_child_name("page0")
    
    def historico_os_selecionado(self, selecionado):
        modelo, linha = selecionado.get_selected()
        if linha:
            self.entra_os_his.set_text(modelo[linha][2])
            self.entra_cliente_his.set_text(modelo[linha][1])
            
    
    def mostrar_tview_historico_os(self):
        self.conecta_db()
        self.liststore_historico_os.clear()
        lista = self.cursor.execute("""SELECT id, cliente, os, data, entrada, total, status FROM os ORDER BY cliente;""")
        total = 0
        for linha in lista:
            if linha[6] == "Quitado":
                total += linha[5]
                self.liststore_historico_os.append(linha)
        
        
        self.entra_total_his.set_text(str(total))
        self.desconecta_db()
    

    ###############################
    ######## Janela Sobre #########
    ############################### 


class Aba_07:
    def botoes_aba_07(self):
        self.btn_voltar_sobre = self.builder.get_object("btn_voltar_sobre")
    
    def liga_botoes_aba_07(self):
        self.btn_voltar_sobre.connect("clicked", self.on_clicked_btn_voltar_sobre)
    

    def on_clicked_btn_voltar_sobre(self, btn):
        self.stack.set_visible_child_name("page0")
            

class Mensagem:
    def mensagem(self, mensagem):
        msg = self.builder.get_object("mensagem")
        lb = self.builder.get_object("lb_erro")

        lb.set_text(mensagem)

        msg.show_all()
        msg.run()
        msg.hide()


class Janela:
    def janela(self):
        arquivo = "janela.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(arquivo)
        self.janela = self.builder.get_object("main")
        self.janela.connect("delete-event", Gtk.main_quit)
