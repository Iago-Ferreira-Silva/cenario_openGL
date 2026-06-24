# ⚽ Estádio de Futebol 3D — OpenGL

Simulação 3D interativa de um estádio de futebol desenvolvida com **Python**, **PyOpenGL** e **Pygame**, como projeto acadêmico da disciplina de Computação Gráfica.

---

## 👥 Equipe

| Nome | Papel |
|---|---|
| Iago Ferreira | Desenvolvedor |
| Antônio Alexandre | Desenvolvedor |
| Daniel Marcelino | Desenvolvedor |
| Vitória Peixoto | Desenvolvedor |

---

## 📋 Sobre o Projeto

O projeto consiste em uma cena 3D interativa que renderiza um estádio de futebol completo, com campo, arquibancadas, gols, torcida, um jogador e uma bola. O usuário pode explorar o ambiente livremente por meio de uma câmera controlável via teclado.

A aplicação utiliza a pipeline de renderização legada do OpenGL (OpenGL 1.x / 2.x) com iluminação de Phong, texturização do gramado, display lists para otimização e projeção perspectiva 3D.

---

## 🏗️ Estrutura do Projeto

```
cenario_openGL/
├── main.py          # Ponto de entrada — loop principal, configuração da janela e orquestração da cena
├── camera.py        # Sistema de câmera livre (yaw, pitch, movimento WASD)
├── stadium.py       # Renderização do estádio: campo, arquibancadas, gols, rede e torcida
├── entities.py      # Entidades da cena: jogador (boneco) e bola de futebol
├── utils.py         # Utilitários: carregamento de textura, iluminação e primitiva draw_cube
├── grass.png        # Textura do gramado aplicada ao campo
└── requirements.txt # Dependências do projeto
```

---

## ✨ Funcionalidades

### 🏟️ Estádio
- **Campo de futebol** com textura de grama e listras alternadas (clara/escura)
- **Demarcações** completas: bordas, linha do meio, círculo central, grande área, pequena área e arcos de penalidade
- **Bandeiras** nos cantos com mastro e flâmula triangular colorida
- **Arquibancadas** em 5 degraus com cores graduais e perspectiva inclinada
- **Cobertura** (teto) sobre as arquibancadas com pilares de sustentação
- **Muros** perimetrais fechando o estádio

### ⚽ Gols
- Dois gols posicionados nas extremidades do campo (z = ±38)
- Traves e travessão renderizados com cubos escalados
- **Rede** gerada por linhas verticais e horizontais cruzadas com profundidade

### 🧍 Jogador (Boneco)
- Personagem articulado construído com cubos (primitiva `draw_cube`)
- Partes modeladas: cabeça, cabelo, tronco, braços (com antebraços), pernas, meias e chuteiras
- Perna direita com rotação de –30° simulando posição de chute
- Braços com inclinações distintas para pose natural
- **Cores**: camisa amarela, short azul, meias brancas, chuteiras e cabelo pretos, pele rosada
- **Sombra** projetada no gramado (quad escurecido no plano y ≈ 0)

### 🔵 Bola
- Esfera branca renderizada com `gluSphere` (32×32 subdivisões)
- Detalhes de costura: 8 discos pretos distribuídos em rotações de 45°
- Sombra circular no gramado usando `GL_POLYGON`

### 👥 Torcida
- Gerada proceduralmente com distribuição aleatória (probabilidade 60%)
- Cada torcedor: cilindro (corpo) + esfera (cabeça) com `gluCylinder` / `gluSphere`
- 8 cores variadas: vermelho, verde, azul, amarelo, branco, laranja, ciano, magenta
- Distribuída nas 4 arquibancadas em 4 degraus
- **Display List** (`glGenLists`) compilada uma única vez na inicialização para máxima performance

### 💡 Iluminação
- Fonte de luz direcional (`GL_LIGHT0`) posicionada em (20, 100, 20)
- Componentes **ambiente** (0.5) e **difusa** (0.9) configuradas
- Specultar desativado para estética cartunesca
- `GL_COLOR_MATERIAL` com `GL_AMBIENT_AND_DIFFUSE` para coloração direta dos objetos
- `GL_SMOOTH` shading (interpolação de normais de Gouraud)

### 🎥 Câmera
- **Posição inicial**: (0, 8, 12) com pitch –30° (visão levemente inclinada para baixo)
- **Rotação horizontal (yaw)**: ←/→ ou A/D
- **Rotação vertical (pitch)**: ↑/↓ ou W/S — limitado ao intervalo [−90°, +90°]
- Velocidade de rotação: 2°/frame | Velocidade de translação: 0.5 unid./frame

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.x | Linguagem principal |
| Pygame-CE | Latest | Janela, eventos, input e carregamento de texturas |
| PyOpenGL | 3.1.7 | Pipeline de renderização 3D (OpenGL + GLU) |

---

## 📦 Instalação e Execução

### Pré-requisitos

- Python 3.8 ou superior
- pip

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd cenario_openGL
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém:

```
pygame-ce
PyOpenGL==3.1.7
```

> **Nota:** Em alguns sistemas pode ser necessário instalar o PyOpenGL Accelerate para melhor performance:
> ```bash
> pip install PyOpenGL_accelerate
> ```

### 3. Execute o projeto

```bash
python main.py
```

---

## 🎮 Controles

| Tecla | Ação |
|---|---|
| `W` / `↑` | Inclinar câmera para cima |
| `S` / `↓` | Inclinar câmera para baixo |
| `A` / `←` | Rotacionar câmera para a esquerda |
| `D` / `→` | Rotacionar câmera para a direita |
| Fechar janela | Encerrar a aplicação |

---

## ⚙️ Configurações Técnicas

| Parâmetro | Valor |
|---|---|
| Resolução da janela | 1280 × 720 px |
| Campo de visão (FOV) | 60° |
| Near clipping plane | 0.1 |
| Far clipping plane | 200.0 |
| Taxa de quadros | 60 FPS |
| Cor de fundo (céu) | RGBA (0.4, 0.75, 1.0) — azul claro |
| Dimensões do campo | 60 × 80 unidades (z: −38 a +38, x: −28 a +28) |

---

## 🧩 Arquitetura e Decisões Técnicas

### Modularização
O código é dividido em módulos com responsabilidades bem definidas, facilitando a manutenção e a divisão de tarefas entre os membros da equipe.

### Display List para a Torcida
A torcida é composta por centenas de objetos geométricos gerados aleatoriamente. Compilá-los em uma Display List (`glGenLists` / `glNewList` / `glCallList`) faz com que a geometria seja processada pela GPU apenas uma vez, reduzindo drasticamente o custo de renderização por frame.

### Primitiva `draw_cube`
A função `draw_cube(x, y, z, width, height, depth, color)` em `utils.py` é a primitiva base de toda a cena. Ela aplica transformações de escala e translação via pilha de matrizes (`glPushMatrix/glPopMatrix`) e renderiza um cubo com normais corretas para iluminação.

### Câmera em primeira pessoa (look-at manual)
Em vez de usar `gluLookAt`, a câmera aplica as rotações e translações diretamente na ModelView matrix (rotação de pitch → yaw → translação negativa), o que é equivalente mas torna o controle mais intuitivo.

### Textura com GL_REPEAT
O gramado usa `GL_TEXTURE_WRAP_S/T = GL_REPEAT` com coordenadas de textura escaladas, produzindo o efeito de repetição da grama sobre toda a superfície do campo.

---

## 📚 Contexto Acadêmico

Projeto desenvolvido como trabalho prático da disciplina de **Computação Gráfica**, com objetivo de aplicar os conceitos de:

- Pipeline de renderização 3D com OpenGL
- Transformações geométricas (translação, rotação, escala)
- Iluminação e sombreamento (modelo de Phong)
- Texturização e mapeamento UV
- Câmera e projeção perspectiva
- Otimização com Display Lists
- Modelagem procedural de cenas complexas