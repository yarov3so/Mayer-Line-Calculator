import numpy as np
import pandas as pd
import re
import statistics as stat
import streamlit as st


def comprehend(mystring):
    mystring=mystring.replace(" ", "")
    data_list=mystring.split(",")
    data =[]
    for el in data_list:
        try:
            data.append(float(el))
        except: 
            for i in range(int(re.findall(r'\d+', el)[0])):
                data.append(None)
    return data
    
datapts=pd.DataFrame(columns=['x', 'y'])
current_entry={0}

st.title("Mayer Line Calculator")
st.markdown("Calculate the equation of the Mayer line of best fit in slope-intercept form.")

entries={}
i=0
while True:
    
    entries[i]=st.text_input("Please enter a pair of coordinates separated by a comma, or write 'done' of you are done. Remember to hit Enter: ",key=i)
    if len(entries[i])==0:
        st.stop()
        break
    if "," not in entries[i]:
        break
    datapts.loc[len(datapts)]=comprehend(entries[i])
    i+=1

if len(datapts)==1:
    st.markdown("You have entered no data points!")
    st.stop()

datapts=datapts.sort_values(by="x")
n=len(datapts)

print("\nYou have entered the following coordinates:")
print(datapts.to_string(index=False))

if len(datapts)%2 == 0:
    
    G1=datapts.iloc[:n//2]
    G2=datapts.iloc[n//2:]

    st.markdown("\nYou have entered an even number of points.")

if len(datapts)%2 == 1:
    
    g1=datapts.iloc[:n//2]
    g2=datapts.iloc[1+n//2:]
    meandist1=((g1-datapts.loc[n//2])['x']**2 + (g1-datapts.loc[n//2])['y']**2).apply(np.sqrt).mean()
    meandist2=((g2-datapts.loc[n//2])['x']**2 + (g2-datapts.loc[n//2])['y']**2).apply(np.sqrt).mean()

    st.markdown("\nYou have entered an odd number of points.")
    
    if meandist1<=meandist2:
    
        st.markdown(f"\nThe middle point {tuple(datapts.loc[n//2])} is closer to the first {n//2} points. Therefore, it is a part of the first group, so we have:")
        
        G1=datapts.iloc[:1+n//2]
        G2=datapts.iloc[1+n//2:]
    
        st.markdown(f"""Group 1:  
        {G1.to_string(index=False)}""")

        st.markdown(f"""Group 2:  
        {G2.to_string(index=False)}""")

    else:

        st.markdown(f"\nThe middle point {tuple(datapts.loc[n//2])} is closer to the last {n//2} points. Therefore, it is a part of the second group, so we have:")
        
        G1=datapts.iloc[:n//2]
        G2=datapts.iloc[n//2:]
    
        st.markdown(f"""Group 1:  
        {G1.to_string(index=False)}""")
    
        st.markdown(f"""Group 2:  
        {G2.to_string(index=False)}""")

M1=(G1['x'].mean(),G1['y'].mean())
M2=(G2['x'].mean(),G2['y'].mean())

st.markdown("As such, we have:")

sumstring_x1=""
for el in G1["x"]:
    sumstring_x1+=(str(el))+" + "
sumstring_x1=sumstring_x1[:-3]

sumstring_y1=""
for el in G1["y"]:
    sumstring_y1+=(str(el))+" + "
sumstring_y1=sumstring_y1[:-3]

sumstring_x2=""
for el in G2["x"]:
    sumstring_x2+=(str(el))+" + "
sumstring_x2=sumstring_x2[:-3]

sumstring_y2=""
for el in G2["y"]:
    sumstring_y2+=(str(el))+" + "
sumstring_y2=sumstring_y2[:-3]

st.markdown(f"""M1 = ( ({sumstring_x1})/{len(G1)} , ({sumstring_y1})/{len(G1)} ) = {M1}  
M2 = ( ({sumstring_x2})/{len(G2)} , ({sumstring_y2})/{len(G2)} ) = {M2}""")

m=(M2[1]-M1[1])/(M2[0]-M1[0])
b=M1[1]-m*M1[0]

st.markdown("We use M1 and M2 to find the slope of the line of best fit by calculating (M2_y - M1_y)/(M2_x - M1_x):")
st.markdown(f"Slope = (M2_y - M1_y)/(M2_x - M1_x) = ({M2[1]} - {M1[1]})/({M2[0]} - {M1[0]}) = {m}")

st.markdown(f"We calculate the y-intercept b by focing the line with slope {m} to pass through either M1 or M2. We will get the same y-intercept no matter which point we choose!")

st.markdown(f"If we choose M1:")
st.markdown(f"""y = mx + b  
y = {m}x + b  
{M1[1]} = {m}*{M1[0]} + b  <-  plugging the coordinates of M1 into the slope-intercept form of the line of best fit.  
b = {M1[1]} - {m}*{M1[0]} = {b}""")

st.markdown(f"If we choose M2:")
st.markdown(f"""y = mx + b  
y = {m}x + b  
{M2[1]} = {m}*{M2[0]} + b  <-  plugging the coordinates of M2 into the slope-intercept form of the line of best fit.  
b = {M2[1]} - {m}*{M2[0]} = {b}""")

st.markdown(f"\nAnd so, the Mayer line method produces the following line of best fit in slope-intercept form: y = {m}x + {b} ")

st.text("")
st.markdown("""*Crafted by yarov3so*   
<a href="https://www.buymeacoffee.com/yarov3so" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="width: 9em; height: auto; padding-top: 0.7em; padding-bottom: 1em" ></a>  
See my other [Math Help Tools](https://mathh3lptools.streamlit.app)""",unsafe_allow_html=True)
