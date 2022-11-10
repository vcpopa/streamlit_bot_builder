import streamlit as st
import sys
sys.path.append("C:\Program Files\Graphviz\bin")
from PIL import Image
import sys
sys.tracebacklimit = 0
import yaml
import os
import traceback
from  scraper import Bot,Actions
from  codegen import CodeGenerator
from flowchart import FlowChart
import SessionState
import graphviz
import nbformat as nbf
from zipfile import ZipFile
from streamlit import caching

st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    with open("./help.yml") as f:
        _help = yaml.safe_load(f)


    st.title("Selenium bot builder")
    image_main = Image.open("./logo.png").resize((800, 200),Image.ANTIALIAS)
    image_side=Image.open("./logo2.png")
    st.image(image_main)
    st.sidebar.image(image_side)
    _scraper_name=['']
    _link_to_scrape=['']
    _download_path=['']
    _action=['']
    _find_by=['']
    _dom_element=['']
    _wait_for=['']
    _keys_to_send=['']
    steps=['Access link']
    ss=SessionState.get(sscraper_name=_scraper_name,slink_to_scrape=_link_to_scrape,sdownload_path=_download_path,saction=_action,sfind_by=_find_by,sdom_element=_dom_element,swait_for=_wait_for,skeys_to_send=_keys_to_send,steps=steps)
    with st.sidebar.form("MAIN BOT CONFIG"):
        
        scraper_name=st.sidebar.text_input("Scraper name",value='Webscraper',help=_help['webscraper']['main']['scraper_name'])
        link_to_scrape=st.sidebar.text_input("Link to scrape",value='...',help=_help['webscraper']['main']['link_to_scrape'])
        download_path=st.sidebar.text_input("Download path",value="path/to/folder",help=_help['webscraper']['main']['download_path'])
        submit_bot_config=st.form_submit_button("Define BOT")
        if submit_bot_config:
            ss.sscraper_name.append(scraper_name)
            ss.slink_to_scrape.append(link_to_scrape)
            ss.sdownload_path.append(download_path)

    with st.form("ACTION CONFIG",clear_on_submit=True):
        
        action=st.selectbox("Select an action type",['Click','Write text','Hit Enter'])
        find_by_box=st.selectbox("Choose DOM element type",['CSS SELECTOR',"XPATH"],help=_help['webscraper']['main']['find_by'])
        dom_element_box=st.text_input("Paste the CSS Selector/XPATH",help=_help['webscraper']['main']['dom_element'])
        wait_for_box=st.text_input("Bot waits for ... seconds after executing command",value=0,help=_help['webscraper']['main']['wait_after_command'])
        keys_to_send_box=st.text_input("Input text",value=None)
        description=st.text_input("Write a a short description",value="Click",help=_help['webscraper']['main']['description'])
        action_submit_button=st.form_submit_button("Add action to bot")

        if action_submit_button:
            
            ss.saction.append(action)
            ss.sfind_by.append(find_by_box)
            ss.sdom_element.append(dom_element_box)
            ss.swait_for.append(wait_for_box)
            ss.skeys_to_send.append(keys_to_send_box)
            ss.steps.append(description)

    if st.button("Create BOT"):

        bot_param_dict={"scraper_name":ss.sscraper_name[len(ss.sscraper_name)-1],"link_to_scrape":ss.slink_to_scrape[len(ss.slink_to_scrape)-1],"download_path":ss.sdownload_path[len(ss.sdownload_path)-1]}
        bot=Bot(param_dict=bot_param_dict)
        template=bot.bot_template()

        actions_param_dicts={"action":ss.saction[1:],"find_by":ss.sfind_by[1:],"dom_element":ss.sdom_element[1:],"wait_for":ss.swait_for[1:],"keys_to_send":ss.skeys_to_send[1:]}
        actions = [dict(zip(actions_param_dicts,t)) for t in zip(*actions_param_dicts.values())]
        for action in actions:
            act=Actions(param_dict=action)
            action_template=act.generate_action_template()
            template=template +"\n"+action_template
        st.subheader("Code preview")
        st.code(template,language='python')

        st.subheader("Process flow")
        dot = graphviz.Digraph(f'{scraper_name}Flow',graph_attr={'rankdir':'LR'},node_attr={'color': 'palegreen3',"shape":"box","style":"rounded,filled"},edge_attr={"style":""},format='png') 
        for step,i in zip(ss.steps,range(len(ss.steps))):
            if len(steps)<=1:
                dot.node(f"{i+1}",step)
            else:
                if i==0:
                    dot.node(f"{i+1}",step)
                else:
                    dot.node(f"{i+1}",step)
                    dot.edge(f"{i}",f"{i+1}")
        st.graphviz_chart(dot)
           
        nb = nbf.v4.new_notebook()
        nb['cells'] = [nbf.v4.new_code_cell(template)]
        nbf.write(nb, f'{scraper_name}.ipynb')
        zip_obj=ZipFile(f"{scraper_name}.zip","w")
        zip_obj.write(f'{scraper_name}.ipynb')
        zip_obj.close()
        with open(f"{scraper_name}.zip","rb") as nb_file:
            st.download_button("Download bot as Jupyter notebook",nb_file,mime='application/zip',file_name=f"{scraper_name}.zip")
            if st.download_button:
                caching.clear_cache()
       

        if st.button("START NEW BOT"):
            
            del ss
            caching.clear_cache()
            main()

if __name__=="__main__":
    try:
        main()
    except:
        st.markdown(traceback.format_exc())
