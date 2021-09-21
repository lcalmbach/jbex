import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

def get_table(tbl_dic: dict) -> str:
    result = '<table>'
    for key, value in tbl_dic.items():
        result += f'<tr><td>{key}</td><td>{value}</td><tr>'

    result += '</table>'
    return result


def get_list_index(lst: list, value):
    try: 
        result = lst.index(value)
    except:
        result = 0
    return result


def make_dic(df: pd.DataFrame, key_col: str, value_col: str):
    keys = df[key_col]
    values = df[value_col]
    result = dict(zip(keys, values))
    return result


def get_href(tit, url):
    result = f'<a href = "{url}" target = "_blank">{tit}</a>'
    return result


def right(text, amount):
    return text[-amount:]


def left(text, amount):
    return text[:amount]
    
def show_table(df:pd.DataFrame, update_mode, height: int, col_cfg:list=[]):
    #Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(groupable=False, value=True, enableRowGroup=False, editable=True)

    if col_cfg != None:
        for col in col_cfg:
            gb.configure_column(col['name'], width=col['width'], visible=col['visible'])
    
    gb.configure_selection('single', use_checkbox=False, rowMultiSelectWithClick=False, suppressRowDeselection=False)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    #Display the grid
    
    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        height=height, 
        width='100%',
        #data_return_mode= DataReturnMode.FILTERED_AND_SORTED, 
        update_mode = update_mode,
        fit_columns_on_grid_load=False,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        enable_enterprise_modules=False,
        )
    df_result = grid_response['data']
    selected = grid_response['selected_rows']
    return selected