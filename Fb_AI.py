import streamlit as st
from streamlit_ace import st_ace
import speech_recognition as sr
from wit import Wit

r = sr.Recognizer()
access_token="56MHVINSJPQIMHIHPGZCOHTPU64ZJUXY"
client = Wit(access_token)
intent=""
entity=""

LANGUAGES = [
    "abap", "abc", "actionscript", "ada", "alda", "apache_conf", "apex", "applescript", "aql", 
    "asciidoc", "asl", "assembly_x86", "autohotkey", "batchfile", "c9search", "c_cpp", "cirru", 
    "clojure", "cobol", "coffee", "coldfusion", "crystal", "csharp", "csound_document", "csound_orchestra", 
    "csound_score", "csp", "css", "curly", "d", "dart", "diff", "django", "dockerfile", "dot", "drools", 
    "edifact", "eiffel", "ejs", "elixir", "elm", "erlang", "forth", "fortran", "fsharp", "fsl", "ftl", 
    "gcode", "gherkin", "gitignore", "glsl", "gobstones", "golang", "graphqlschema", "groovy", "haml", 
    "handlebars", "haskell", "haskell_cabal", "haxe", "hjson", "html", "html_elixir", "html_ruby", "ini", 
    "io", "jack", "jade", "java", "javascript", "json", "json5", "jsoniq", "jsp", "jssm", "jsx", "julia", 
    "kotlin", "latex", "less", "liquid", "lisp", "livescript", "logiql", "logtalk", "lsl", "lua", "luapage", 
    "lucene", "makefile", "markdown", "mask", "matlab", "maze", "mediawiki", "mel", "mixal", "mushcode", 
    "mysql", "nginx", "nim", "nix", "nsis", "nunjucks", "objectivec", "ocaml", "pascal", "perl", "perl6", 
    "pgsql", "php", "php_laravel_blade", "pig", "plain_text", "powershell", "praat", "prisma", "prolog", 
    "properties", "protobuf", "puppet", "python", "qml", "r", "razor", "rdoc", "red", "redshift", "rhtml", 
    "rst", "ruby", "rust", "sass", "scad", "scala", "scheme", "scss", "sh", "sjs", "slim", "smarty", 
    "snippets", "soy_template", "space", "sparql", "sql", "sqlserver", "stylus", "svg", "swift", "tcl", 
    "terraform", "tex", "text", "textile", "toml", "tsx", "turtle", "twig", "typescript", "vala", "vbscript", 
    "velocity", "verilog", "vhdl", "visualforce", "wollok", "xml", "xquery", "yaml"
]

THEMES = [
    "github","ambiance", "chaos", "chrome", "clouds", "clouds_midnight", "cobalt", "crimson_editor", "dawn",
    "dracula", "dreamweaver", "eclipse","gob", "gruvbox", "idle_fingers", "iplastic",
    "katzenmilch", "kr_theme", "kuroir", "merbivore", "merbivore_soft", "mono_industrial", "monokai",
    "nord_dark", "pastel_on_dark", "solarized_dark", "solarized_light", "sqlserver", "terminal",
    "textmate", "tomorrow", "tomorrow_night", "tomorrow_night_blue", "tomorrow_night_bright",
    "tomorrow_night_eighties", "twilight", "vibrant_ink", "xcode"
]

KEYBINDINGS = [
    "sublime","emacs","vim", "vscode"
]

def output(intent,entity):
    if intent == 'create_list':
        return f"{entity} = []"
    elif intent=="range":
        return f"range({entity})" 
    elif intent=="sort_ascending":
        return f"sorted_list = {entity}.sort()"
    elif intent=="list_max":
        return f"max_element=max({entity})"
    elif intent=="list_len":
        return f"length=len({entity})" 
    elif intent=="list_reverse":
        return f"reverse_list={entity}.reverse()"
    else:
        return "#Instruct with voice" 


st.title('VOCAI')
st.sidebar.title(":memo: Voice Code Editor :smile:") 
st.text('Editor')   
content = st_ace(
        placeholder= "Enter your code",
        height = 250,
        language=st.sidebar.selectbox("Select Language.", options=LANGUAGES),
        theme=st.sidebar.selectbox("Editor Theme.", options=THEMES),
        keybinding=st.sidebar.selectbox("Keybinding mode.", options=KEYBINDINGS),
        font_size=st.sidebar.slider("Font size.", 5, 24, 12),
        tab_size=st.sidebar.slider("Tab size.", 1, 8, 4),
        show_gutter=st.sidebar.checkbox("Show gutter.", value=True),
        show_print_margin=st.sidebar.checkbox("Show print margin.", value=True),
        key="ace-editor1",
        wrap=True
    )

MyText=""
with open("code.txt") as file:
    MyText = file.read()

if st.button('Start recording'):
    try:
        with sr.Microphone() as source2:
            with st.spinner('Recording Started...'):
                r.adjust_for_ambient_noise(source2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                response = client.message(MyText)
                intent = response['intents'][0]['name']
                entity = response['entities']['list_name:list_name'][0]['value']
                #print(response)

                with open("code.txt","w") as file:
                    file.write(output(intent,entity))
        
    except error as e:
        st.text('Error recording your voice. Please try again')    

if len(MyText)>0:
    st_ace(value=output(intent,entity),height=50)

if st.button('Clear Cache'):
    with open("code.txt","w") as file:
        file.write("")

if st.button('Save Editor Code'):
    with open('editor.txt',"w") as file:
        file.write(content)