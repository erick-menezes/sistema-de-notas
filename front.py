from tkinter import *
from tkinter import TclError
from tkinter import font
import tkinter.ttk as ttk
import tkinter.messagebox as msb

import db

colors = {
    "mainBg": "SteelBlue1",
    "mainBgLight": "dodger blue",
    "turquoise": "turquoise3",
    "blueMedium": "DodgerBlue3",
    "white": "white smoke",
    "gray": "gray64",
    "red": "red3",
    "darkRed": "red4",
    "green": "sea green",
    "darkGreen": "dark green",
    "black": "gray10",
    "yellow": "gold",
    "blue": "RoyalBlue2"
}

fonts = {
    "heading": ("Segoe UI Semibold", 18, "bold"),
    "formText": ("Segoe UI Semibold", 10, "bold"),
    "labelForm": ("Segoe UI Semibold", 14, "bold"),
    "paragraph": ("Segoe UI Semibold", 10),
    "button": ("Gill Sans", 10, "bold"),
}

root = Tk()
root.title("Sistema de Notas")
root.iconphoto(False, PhotoImage(file="./assets/icon.png"))

sc_width = root.winfo_screenwidth()
sc_height = root.winfo_screenheight()

width = 900
height = 640

x = (sc_width/2) - (width/2)
y = (sc_height/2) - (height/2)

root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg=colors["mainBg"])

insertWindow = None
editWindow = None

id = None
studentEnrollment = IntVar()
studentName = StringVar()
subject = StringVar()
grade1 = DoubleVar()
grade2 = DoubleVar()
grade3 = DoubleVar()
gradeAvd = DoubleVar()
gradeAvds = DoubleVar()
situation = ""

insertButton = None
editButton = None

averageResult = None

def hoverIn(color):
    if color == "mainGreen":
        insertBtn["bg"] = colors["darkGreen"]
    elif color == "insertGreen":
        insertButton["bg"] = colors["darkGreen"]
    elif color == "editGreen":
        editButton["bg"] = colors["darkGreen"]
    elif color == "red":
        deleteBtn["bg"] = colors["darkRed"]
    else:
        print("Erro: Botão não identificado.")

def hoverOut(color):
    if color == "mainGreen":
        insertBtn["bg"] = colors["green"]
    elif color == "insertGreen":
        insertButton["bg"] = colors["green"]
    elif color == "editGreen":
        editButton["bg"] = colors["green"]
    elif color == "red":
        deleteBtn["bg"] = colors["red"]
    else:
        print("Erro: Botão não identificado.")

def view():
    fetch = db.database()

    for data in fetch:
        tree.insert('', 'end', values=(data))

def openInsertWindow():

    studentEnrollment.set("")
    studentName.set("")
    subject.set("")

    def calculateAverage(event):
        global situation

        av1Input = grade1Input.get()
        av2Input = grade2Input.get()
        av3Input = grade3Input.get()
        avdInput = gradeAvd.get()
        avdsInput = gradeAvds.get()

        if av1Input == '':
            av1Input = 0
        elif av2Input == '':
            av2Input = 0
        elif av3Input == '':
            av3Input = 0
        elif avdInput == '':
            avdInput = 0
        elif avdsInput == '':
            avdsInput = 0

        try:
            av1 = float(av1Input)
            av2 = float(av2Input)
            av3 = float(av3Input)
            avd = float(avdInput)
            avds = float(avdsInput)

            if av1 < 4 and av2 > av1 and av3 > av1:
                if avd > avds:
                    calculatedAverage = (av2 + av3 + avd)/3
                else:
                    calculatedAverage = (av2 + av3 + avds)/3
            elif av1 > av2 and av2 < 4 and av3 > av2:
                if avd > avds:
                    calculatedAverage = (av1 + av3 + avd)/3
                else:
                    calculatedAverage = (av1 + av3 + avds)/3
            elif av1 > 4 and av2 > 4 and av3 > av1:
                if avd > avds:
                    calculatedAverage = (av2 + av3 + avd)/3
                else:
                    calculatedAverage = (av2 + av3 + avds)/3
            elif av1 > 4 and av2 > 4 and av3 > av2:
                if avd > avds:
                    calculatedAverage = (av1 + av3 + avd)/3
                else:
                    calculatedAverage = (av1 + av3 + avds)/3
            else:
                if avd > avds:
                    calculatedAverage = (av1 + av2 + avd)/3
                else:
                    calculatedAverage = (av1 + av2 + avds)/3

            if calculatedAverage > 6.0:
                averageResult["fg"] = colors["green"]
                situation = "Aprovado"
            elif calculatedAverage < 6.0:
                averageResult["fg"] = colors["red"]
                situation = "Reprovado"
            else:
                averageResult["fg"] = colors["yellow"]
                situation = "Aprovado"
            
            averageResult["text"] = "%.1f" % calculatedAverage
            averageResult["font"] = fonts["labelForm"]
        except Exception as ValueError:
            print("Digite apenas números, por gentileza.")

    global insertWindow
    global insertButton
    global averageResult
    insertWindow = Toplevel()
    insertWindow.title("Inserir nota")
    insertWindow.iconphoto(False, PhotoImage(file="./assets/insert.png"))
    width = 500
    height = 340
    sc_width = insertWindow.winfo_screenwidth()
    sc_height = insertWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    
    insertWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    insertWindow.resizable(0, 0)
    insertWindow.config(bg=colors["mainBg"])

    titleInsert = Label(
        insertWindow, 
        text="INSERIR NOTA",
        pady=5, 
        font=fonts["heading"], 
        bg=colors["mainBgLight"], 
        fg=colors["white"]
    )
    titleInsert.pack(fill=X)

    formContainer = Frame(
        insertWindow,
        pady=20,
        padx=5,
        bg=colors["mainBg"]
    )
    formContainer.pack()

    enrollmentLabel = Label(
        formContainer, 
        text="Matrícula do aluno: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    enrollmentLabel.grid(row=0, column=0)

    enrollmentInput = Entry(
        formContainer, 
        textvariable=studentEnrollment, 
        width=27, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    enrollmentInput.grid(row=0, column=1)

    nameLabel = Label(
        formContainer, 
        text="Nome do aluno: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    nameLabel.grid(row=1, column=0)

    nameInput = Entry(
        formContainer, 
        textvariable=studentName, 
        width=27, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    nameInput.grid(row=1, column=1)

    subjectLabel = Label(
        formContainer, 
        text="Matéria: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    subjectLabel.grid(row=2, column=0)

    subjectInput = ttk.Combobox(
        formContainer, 
        textvariable=subject, 
        width=15, 
        font=("bold")
    )
    subjectInput['values'] = (
        'Matemática',
        'História',
        'Geografia',
        'Química',
        'Física',
        'Educação Física',
    )
    subjectInput.grid(row=2, column=1)
    
    grade1Label = Label(
        formContainer, 
        text="Nota da AV1: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    grade1Label.grid(row=3, column=0)

    grade1Input = Entry(
        formContainer, 
        textvariable=grade1, 
        width=4, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    grade1Input.bind("<KeyRelease>", calculateAverage)
    grade1Input.grid(row=3, column=1)

    grade2Label = Label(
        formContainer, 
        text="Nota da AV2: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    grade2Label.grid(row=4, column=0)

    grade2Input = Entry(
        formContainer, 
        textvariable=grade2, 
        width=4, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    grade2Input.bind("<KeyRelease>", calculateAverage)
    grade2Input.grid(row=4, column=1)

    grade3Label = Label(
        formContainer, 
        text="Nota da AV3: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    grade3Label.grid(row=5, column=0)

    grade3Input = Entry(
        formContainer, 
        textvariable=grade3, 
        width=4, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    grade3Input.bind("<KeyRelease>", calculateAverage)
    grade3Input.grid(row=5, column=1)

    avdLabel = Label(
        formContainer, 
        text="Nota da AVD: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    avdLabel.grid(row=6, column=0)

    avdInput = Entry(
        formContainer, 
        textvariable=gradeAvd, 
        width=4, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    avdInput.bind("<KeyRelease>", calculateAverage)
    avdInput.grid(row=6, column=1)

    avdsLabel = Label(
        formContainer, 
        text="Nota da AVD: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    avdsLabel.grid(row=7, column=0)

    avdsInput = Entry(
        formContainer, 
        textvariable=gradeAvds, 
        width=4, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    avdsInput.bind("<KeyRelease>", calculateAverage)
    avdsInput.grid(row=7, column=1)

    averageLabel = Label(
        formContainer, 
        text="Nota Final: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    averageLabel.grid(row=8, column=0)

    averageResult = Label(
        formContainer,
        text="Insira as notas de AV1 e AV2 para calcular a média.",
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    averageResult.grid(row=8, column=1)

    insertButton = Button(
        insertWindow, 
        text="Inserir",
        bg=colors["green"],
        fg=colors["white"],
        font=fonts["button"],
        cursor="hand2",
        bd=0,
        padx=30,
        pady=5,
        command=insertGrade
    )
    insertButton.pack()
    insertButton.bind("<Enter>", lambda event: hoverIn("insertGreen"))
    insertButton.bind("<Leave>", lambda event: hoverOut("insertGreen"))

def insertGrade():
    global averageResult

    try:
        if studentEnrollment.get() == "" or studentName.get() == "" or subject.get() == "" or grade1.get() == "" or grade2.get() == "" or grade3.get() == "" or gradeAvd.get() == "" or gradeAvds.get() == "":
            msb.showwarning("Preencha todos os campos", "Preencha todos os campos para poder prosseguir, por favor.", parent=insertWindow)
        elif len(str(studentEnrollment.get())) != 12:
            msb.showerror("Matrícula inválida", "A matrícula deve possuir 12 números, tente novamente.", parent=insertWindow)
        else:
            tree.delete(*tree.get_children())
            
            fetch = db.insert(
                studentEnrollment.get(),
                studentName.get(), 
                subject.get(), 
                str(grade1.get()), 
                str(grade2.get()),
                str(grade3.get()),
                str(gradeAvd.get()),
                str(gradeAvds.get()),
                str(averageResult["text"]),
                situation
            )

            for data in fetch:
                tree.insert('', 'end', values=(data))
            
            studentEnrollment.set("")
            studentName.set("")
            subject.set("")
            grade1.set("")
            grade2.set("")
            grade3.set("")
            gradeAvd.set("")
            gradeAvds.set("")
            averageResult["text"] = "Insira as notas de AV1 e AV2 para calcular a média."
            averageResult["fg"] = colors["white"]
            averageResult["font"] = fonts["formText"]

    except TclError as e:
        msb.showwarning("Preencha todos os campos", "Preencha todos os campos para poder prosseguir, por favor.", parent=insertWindow)
            
def removeGrade():
    if not tree.selection():
        msb.showwarning("Nenhum item selecionado", "Selecione um item da lista para remover.")
    else:
        question = msb.askyesno("Remover nota", "Tem certeza que deseja remover esta nota?")
        if question == True:
            selectItem = tree.selection()

            for item in selectItem:
                data = tree.item(item)["values"]
                
                tree.delete(item)
                db.delete(data[0], data[2])

def editGrade():
    global averageResult

    try:
        if studentEnrollment.get() == "" or studentName.get() == "" or subject.get() == "" or grade1.get() == "" or grade2.get() == "" or grade3.get() == "" or gradeAvd.get() == "" or gradeAvds.get() == "":
            msb.showwarning("Preencha todos os campos", "Preencha todos os campos para poder prosseguir, por favor.", parent=insertWindow)
        elif len(str(studentEnrollment.get())) != 12:
            msb.showerror("Matrícula inválida", "A matrícula deve possuir 12 números, tente novamente.", parent=insertWindow)
        else:
            tree.delete(*tree.get_children())
            
            fetch = db.update(
                studentEnrollment.get(),
                studentName.get(),
                subject.get(),
                str(grade1.get()),
                str(grade2.get()),
                str(grade3.get()),
                str(gradeAvd.get()),
                str(gradeAvds.get()),
                str(averageResult["text"]),
                situation
            )

            for data in fetch:
                tree.insert('', 'end', values=(data))
            
            studentEnrollment.set("")
            studentName.set("")
            subject.set("")
            grade1.set("")
            grade2.set("")
            grade3.set("")
            gradeAvd.set("")
            gradeAvds.set("")
            averageResult["text"] = "Insira as notas de AV1 e AV2 para calcular a média."
            averageResult["fg"] = colors["white"]
            averageResult["font"] = fonts["formText"]

            editWindow.destroy()
    except TclError as e:
        msb.showwarning("Preencha todos os campos", "Preencha todos os campos para poder prosseguir, por favor.", parent=editWindow)
    db.update()

def openEditWindow(event):
    global editWindow, editButton, studentEnrollment, studentName, subject, grade1, grade2, grade3, gradeAvd, gradeAvds, averageResult, situation

    def calculateAverage(event):
        global situation

        av1Input = grade1Input.get()
        av2Input = grade2Input.get()
        av3Input = grade3Input.get()
        avdInput = gradeAvd.get()
        avdsInput = gradeAvds.get()

        if av1Input == '':
            av1Input = 0
        elif av2Input == '':
            av2Input = 0
        elif av3Input == '':
            av3Input = 0
        elif avdInput == '':
            avdInput = 0
        elif avdsInput == '':
            avdsInput = 0

        try:
            av1 = float(av1Input)
            av2 = float(av2Input)
            av3 = float(av3Input)
            avd = float(avdInput)
            avds = float(avdsInput)

            if av1 < 4 and av2 > av1 and av3 > av1:
                if avd > avds:
                    calculatedAverage = (av2 + av3 + avd)/3
                else:
                    calculatedAverage = (av2 + av3 + avds)/3
            elif av1 > av2 and av2 < 4 and av3 > av2:
                if avd > avds:
                    calculatedAverage = (av1 + av3 + avd)/3
                else:
                    calculatedAverage = (av1 + av3 + avds)/3
            elif av1 > 4 and av2 > 4 and av3 > av1:
                if avd > avds:
                    calculatedAverage = (av2 + av3 + avd)/3
                else:
                    calculatedAverage = (av2 + av3 + avds)/3
            elif av1 > 4 and av2 > 4 and av3 > av2:
                if avd > avds:
                    calculatedAverage = (av1 + av3 + avd)/3
                else:
                    calculatedAverage = (av1 + av3 + avds)/3
            else:
                if avd > avds:
                    calculatedAverage = (av1 + av2 + avd)/3
                else:
                    calculatedAverage = (av1 + av2 + avds)/3

            if calculatedAverage > 6.0:
                averageResult["fg"] = colors["green"]
                situation = "Aprovado"
            elif calculatedAverage < 6.0:
                averageResult["fg"] = colors["red"]
                situation = "Reprovado"
            else:
                averageResult["fg"] = colors["yellow"]
                situation = "Aprovado"
            
            averageResult["text"] = "%.1f" % calculatedAverage
            averageResult["font"] = fonts["labelForm"]
            
        except Exception as ValueError:
            print("Digite apenas números, por gentileza.")

    
    selectedItem = tree.focus()
    data = tree.item(selectedItem)["values"]
    
    fetch = db.select(data[0], data[2])

    studentEnrollment.set("")
    studentName.set("")
    subject.set("")
    grade1.set("")
    grade2.set("")
    grade3.set("")
    gradeAvd.set("")
    gradeAvds.set("")

    studentEnrollment.set(data[0])
    studentName.set(data[1])
    subject.set(data[2])
    grade1.set(data[3])
    grade2.set(data[4])
    grade3.set(data[5])
    gradeAvd.set(data[6])
    gradeAvds.set(data[7])
    situation = data[9]

    editWindow = Toplevel()
    editWindow.title("Teste")
    editWindow.iconphoto(False, PhotoImage(file="./assets/edit.png"))

    width = 500
    height = 340
    sc_width = editWindow.winfo_screenwidth()
    sc_height = editWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    
    editWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    editWindow.resizable(0, 0)
    editWindow.config(bg=colors["mainBg"])

    titleEdit = Label(
        editWindow, 
        text="EDITAR NOTA",
        pady=5, 
        font=fonts["heading"], 
        bg=colors["mainBgLight"], 
        fg=colors["white"]
    )
    titleEdit.pack(fill=X)

    formContainer = Frame(
        editWindow,
        pady=20,
        padx=5,
        bg=colors["mainBg"]
    )
    formContainer.pack()

    enrollmentLabel = Label(
        formContainer, 
        text="Matrícula do aluno: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    enrollmentLabel.grid(row=0, column=0)

    enrollmentInput = Entry(
        formContainer, 
        textvariable=studentEnrollment, 
        width=27, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    enrollmentInput.grid(row=0, column=1)

    nameLabel = Label(
        formContainer, 
        text="Nome do aluno: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    nameLabel.grid(row=1, column=0)

    nameInput = Entry(
        formContainer, 
        textvariable=studentName, 
        width=27, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    nameInput.grid(row=1, column=1)

    subjectLabel = Label(
        formContainer, 
        text="Matéria: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    subjectLabel.grid(row=2, column=0)

    subjectInput = ttk.Combobox(
        formContainer, 
        textvariable=subject, 
        width=15, 
        font=("bold")
    )
    subjectInput['values'] = (
        'Matemática',
        'História',
        'Geografia',
        'Química',
        'Física',
        'Educação Física',
    )
    subjectInput.grid(row=2, column=1)
    
    grade1Label = Label(
        formContainer, 
        text="Nota da AV1: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    grade1Label.grid(row=3, column=0)

    grade1Input = Entry(
        formContainer, 
        textvariable=grade1, 
        width=4, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    grade1Input.bind("<KeyRelease>", calculateAverage)
    grade1Input.grid(row=3, column=1)

    grade2Label = Label(
        formContainer, 
        text="Nota da AV2: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    grade2Label.grid(row=4, column=0)

    grade2Input = Entry(
        formContainer, 
        textvariable=grade2, 
        width=4, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    grade2Input.bind("<KeyRelease>", calculateAverage)
    grade2Input.grid(row=4, column=1)

    grade3Label = Label(
        formContainer, 
        text="Nota da AV3: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    grade3Label.grid(row=5, column=0)

    grade3Input = Entry(
        formContainer, 
        textvariable=grade3, 
        width=4, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    grade3Input.bind("<KeyRelease>", calculateAverage)
    grade3Input.grid(row=5, column=1)

    avdLabel = Label(
        formContainer, 
        text="Nota da AVD: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    avdLabel.grid(row=6, column=0)

    avdInput = Entry(
        formContainer, 
        textvariable=gradeAvd, 
        width=4, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    avdInput.bind("<KeyRelease>", calculateAverage)
    avdInput.grid(row=6, column=1)

    avdsLabel = Label(
        formContainer, 
        text="Nota da AVD: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    avdsLabel.grid(row=7, column=0)

    avdsInput = Entry(
        formContainer, 
        textvariable=gradeAvds, 
        width=4, 
        bd=0, 
        fg=colors["black"], 
        font=("bold")
    )
    avdsInput.bind("<KeyRelease>", calculateAverage)
    avdsInput.grid(row=7, column=1)

    averageLabel = Label(
        formContainer, 
        text="Nota Final: ", 
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    averageLabel.grid(row=8, column=0)

    averageResult = Label(
        formContainer,
        text="Insira as notas de AV1 e AV2 para calcular a média.",
        bg=colors["mainBg"], 
        fg=colors["white"], 
        font=fonts["formText"]
    )
    averageResult.grid(row=8, column=1)

    averageResult["text"] = fetch[0][8]

    editButton = Button(
        editWindow, 
        text="Inserir",
        bg=colors["green"],
        fg=colors["white"],
        font=fonts["button"],
        cursor="hand2",
        bd=0,
        padx=30,
        pady=5,
        command=editGrade
    )
    editButton.pack()
    editButton.bind("<Button>", lambda event: calculateAverage)
    editButton.bind("<Enter>", lambda event: hoverIn("editGreen"))
    editButton.bind("<Leave>", lambda event: hoverOut("editGreen"))
            

header = Frame(root)
header.pack(fill=X)

title = Label(
    header, 
    text="SISTEMA DE NOTAS DA TURMA",
    pady=20, 
    font=fonts["heading"], 
    bg=colors["mainBgLight"], 
    fg=colors["white"]
)
title.pack(fill=X)

body = Frame(
    root,
    bg=colors["mainBg"],
    pady=15,
    padx=15
)
body.pack(fill=BOTH)

btnContainer = Frame(body, bg=colors["mainBg"])
btnContainer.pack()

insertBtn = Button(
    btnContainer, 
    text="Adicionar nota",
    bg=colors["green"],
    fg=colors["white"],
    font=fonts["button"],
    cursor="hand2",
    bd=0,
    padx=15,
    height=2,
    command=openInsertWindow,
)

insertBtn.pack(side=LEFT)
insertBtn.bind("<Enter>", lambda event: hoverIn("mainGreen"))
insertBtn.bind("<Leave>", lambda event: hoverOut("mainGreen"))

btnMargin = Frame(
    btnContainer,
    bg=colors["mainBg"],
    width=10
)
btnMargin.pack(side=LEFT)

deleteBtn = Button(
    btnContainer, 
    text="Remover nota",
    bg=colors["red"],
    fg=colors["white"],
    font=fonts["button"],
    cursor="hand2",
    bd=0,
    padx=15,
    height=2,
    command=removeGrade
)
deleteBtn.pack(side=LEFT)
deleteBtn.bind("<Enter>", lambda event: hoverIn("red"))
deleteBtn.bind("<Leave>", lambda event: hoverOut("red"))

tablePadding = Frame(
    body,
    bg=colors["mainBg"],
    height=10
)
tablePadding.pack()

tableContainer = Frame(body)
tableContainer.pack()

ScrollbarX = Scrollbar(tableContainer, orient=HORIZONTAL)
ScrollbarY = Scrollbar(tableContainer, orient=VERTICAL)

tree = ttk.Treeview(
    tableContainer, 
    columns=("Matrícula", "Nome do aluno", "Matéria", "AV1", "AV2", "AV3", "AVD", "AVDS", "Nota Final", "Situação"),
    height=17,
    selectmode="extended",
    yscrollcommand=ScrollbarY.set,
    xscrollcommand = ScrollbarX.set
)

ScrollbarY.config(command=tree.yview)
ScrollbarY.pack(side=RIGHT, fill=Y)
ScrollbarX.config(command=tree.xview)
ScrollbarX.pack(side=BOTTOM, fill=X)

tree.heading("Matrícula", text="Matrícula", anchor=W)
tree.heading("Nome do aluno", text="Nome do aluno", anchor=W)
tree.heading("Matéria", text="Matéria", anchor=W)
tree.heading("AV1", text="AV1", anchor=W)
tree.heading("AV2", text="AV2", anchor=W)
tree.heading("AV3", text="AV3", anchor=W)
tree.heading("AVD", text="AVD", anchor=W)
tree.heading("AVDS", text="AVDS", anchor=W)
tree.heading("Nota Final", text="Nota Final", anchor=W)
tree.heading("Situação", text="Situação", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=140, anchor=CENTER)
tree.column('#2', stretch=NO, minwidth=0, width=190, anchor=CENTER)
tree.column('#3', stretch=NO, minwidth=0, width=140, anchor=CENTER)
tree.column('#4', stretch=NO, minwidth=0, width=70, anchor=CENTER)
tree.column('#5', stretch=NO, minwidth=0, width=70, anchor=CENTER)
tree.column('#6', stretch=NO, minwidth=0, width=70, anchor=CENTER)
tree.column('#7', stretch=NO, minwidth=0, width=70, anchor=CENTER)
tree.column('#8', stretch=NO, minwidth=0, width=70, anchor=CENTER)
tree.column('#9', stretch=NO, minwidth=0, width=70, anchor=CENTER)
tree.column('#10', stretch=NO, minwidth=0, width=80, anchor=CENTER)

tree.pack(fill=X)

tree.bind('<Double-Button-1>', openEditWindow)

footer = Frame(
    root,
    bg=colors["blue"],
    width=20,
    pady=10
)
footer.pack(fill=X)

infoLabel = Label(
    footer,
    text="Para editar uma nota já inserida, clique duas vezes na mesma.",
    bg=colors["blue"],
    fg=colors["white"],
    font=fonts["labelForm"]
)
infoLabel.pack()

infoContainer = Frame(
    footer,
    pady=2,
    bg=colors["blue"],
)
infoContainer.pack(fill=X)

infoLabel2 = Label(
    infoContainer,
    text="Pressione Ctrl para selecionar e remover mais de um item.",
    bg=colors["blue"],
    fg=colors["white"],
    font=fonts["labelForm"]
)
infoLabel2.pack()

if __name__ == '__main__':
    view()
    root.mainloop()