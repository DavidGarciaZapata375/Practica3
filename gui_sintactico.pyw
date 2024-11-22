import sys
import re
from gui_sintactico_ui import *
from PyQt5.QtWidgets import *
from nltk import CFG, ChartParser, Tree


class Ventana(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btn_derivar_izquierda.clicked.connect(self.derivar_izquierda)
        self.ui.btn_derivar_derecha.clicked.connect(self.derivar_derecha)

        self.gramatica = CFG.fromstring("""
        E -> E '+' T | E '-' T | T
        T -> T '*' F | T '/' F | F
        F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
        """)

        self.ui.lbl_gramatica.setText("""
        E -> E '+' T | E '-' T | T
        T -> T '*' F | T '/' F | F
        F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
        """)

        # Crear un parser usando la gramática
        self.parser = ChartParser(self.gramatica)

    def derivar_izquierda(self):
        # Actualizar la expresión objetivo antes de derivar
        expresion = self.ui.text_input.toPlainText()
        self.expresion_objetivo = self.tokenizar_expresion(expresion)

        pasos_izquierda = []
        for tree in self.parser.parse(self.expresion_objetivo):
            print("Derivación por la izquierda:")
            pasos_izquierda = self.mostrar_derivacion(tree, orden="izquierda")
            if pasos_izquierda:
                pasos_izquierda_str = "\n".join(pasos_izquierda)
            else:
                pasos_izquierda_str = "No se encontraron derivaciones"

            self.ui.lbl_derivacion.setText("Derivación por izquierda:\n" + pasos_izquierda_str)
            print(pasos_izquierda)
            self.mostrar_arbol(tree)

    def derivar_derecha(self):
        # Actualizar la expresión objetivo antes de derivar
        expresion = self.ui.text_input.toPlainText()
        self.expresion_objetivo = self.tokenizar_expresion(expresion)

        pasos_derecha = []
        for tree in self.parser.parse(self.expresion_objetivo):
            print("\nDerivación por la derecha:")
            pasos_derecha = self.mostrar_derivacion(tree, orden="derecha")
            if pasos_derecha:
                pasos_derecha_str = "\n".join(pasos_derecha)
            else:
                pasos_derecha_str = "No se encontraron derivaciones"

            self.ui.lbl_derivacion.setText("Derivación por derecha:\n" + pasos_derecha_str)
            print(pasos_derecha)
            self.mostrar_arbol(tree)

    def tokenizar_expresion(self, expresion):
        """
        Tokeniza la entrada separando operadores, paréntesis y operandos.
        """
        # Usar una expresión regular para dividir en tokens
        tokens = re.findall(r'\d+|[a-zA-Z]+|[()+\-*/]', expresion)
        print("Tokens generados:", tokens)  # Depuración
        return tokens

    def mostrar_derivacion(self, arbol, orden="izquierda"):
        pasos = []

        def recorrer_subarbol(subarbol):
            if isinstance(subarbol, str):
                return subarbol

            produccion = f"{subarbol.label()} -> " + " ".join(
                child.label() if isinstance(child, Tree) else str(child) for child in subarbol
            )
            pasos.append(produccion)

            hijos = subarbol if orden == "izquierda" else reversed(subarbol)
            for child in hijos:
                if isinstance(child, Tree):
                    recorrer_subarbol(child)

        recorrer_subarbol(arbol)
        return pasos

    def mostrar_arbol(self, tree):
        """
        Muestra el árbol de derivación en la consola y en una ventana gráfica.
        """
        print("Árbol de derivación:")
        tree.pretty_print()
        tree.draw()


if __name__ == "__main__":
    mi_aplicacion = QApplication(sys.argv)
    mi_app = Ventana()
    mi_app.show()
    sys.exit(mi_aplicacion.exec_())
