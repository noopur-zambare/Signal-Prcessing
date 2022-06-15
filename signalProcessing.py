import pandas as pd
import math
import matplotlib.pyplot as plt


#------------             retreving data from excel file             ----------#

excel_file = '/ata.csv.xlsx'
data = pd.read_excel(excel_file)

#------------      variables for storing signals and other data      ----------#

signal_x = data['x[n]']  # original signal x[n]
signal_y = data['y[n]']  # original signal y[n]

time_axis = [i for i in range(193)]   # x axis for the samples of the signals


dtft_of_signal_y = []
dtft_of_signal_x = []
dtft_of_impulse_response = []
dtft_of_denoised_signal = []

denoised_signal = []
deblured_signal = []
recovered_signal = []

#------------                  defining functions                    ----------#

def hn(n):                           # impulse response as a function of n
    if n == -2:                      # h[n]= 1/16[1,4,6,4,1]
        return 1/16                  # where when n= 0 , h[0] = 6/16
    elif n == -1:
        return 4/16
    elif n == -0:
        return 6/16
    elif n == 1:
        return 4/16
    elif n == 2:
        return 1/16

def dtft_of_hn():                    # dtft of impulse response
    for k in range(193):             # loop k runs for frequency
        sum =0
        for n in range(-2,3):
            sum+= hn(n) *(math.e)**(-1j*(2*math.pi*k/193)*n)
        dtft_of_impulse_response.append(round(sum.real,4) + round(sum.imag,4)* 1j)
    return dtft_of_impulse_response                      # returns a list dtft_of_impulse_response which has the data of dtft of hn

def dtft(signal,array):              # dtft of any signal, it takes an array as a parameter to store the data
    for k in range(193):             # loop k runs over the frequency
        sum =0
        for n in range(len(signal)):
            sum+= signal[n] *(math.e)**(-1j*(2*math.pi*k/193)*n)
        array.append(round(sum.real,4) + round(sum.imag,4)* 1j)
    return array                     # returns the array with the data of dtft of that signal

def ift(signal,array):               # inverse fourier transform of any signa,it takes an array as a parameter to store the data
    for k in range(len(signal)):
        sum =0
        for n in range(193):
            sum += signal[n] * (math.e)**((1j*2*math.pi*k*n)/193)
        sum = (sum/193)
        array.append((sum))
    return  array                    # returns the array with the data of dtft of that signal


def array(k):                       # function for making an array for convolution purpose
    if -2<=k<=2:
        return 1/5
    else: return 0
#------------                       Question1                       ----------#

def denoise(signal):                # function to denoise any signal by convolving it with the array function
    for n in range(193):
        sum = 0
        for k in range(193):
            sum+= signal[k]*array(n - k)
        denoised_signal.append(sum)  # stores the result in the denoised signal array
denoise(signal_y)      # denoising signal y[n]

# code block to plot the denoised y[n]
'''
plt.title('Denoised signal')
plt.plot(time_axis,denoised_signal,'g')
plt.show()
'''

dtft_of_hn()   # calling the function for doing the dtft of impulse response
dtft(denoised_signal,dtft_of_denoised_signal)  # dtft of the denoised_signal and storing the output in dtft_of_denoised_signal

for i in range(193):    # clipping the dtft of impulse respose
    if abs((dtft_of_impulse_response[i])) < 0.4:
        dtft_of_impulse_response[i]=(0.4)

for i in range(len(dtft_of_denoised_signal)):   # dividing the dtft of the denoised signal and impulse response and storing the result in array deblured_signal
    div =0
    div = (dtft_of_denoised_signal[i]) / dtft_of_impulse_response[i]
    deblured_signal.append(div)

#------------                 recovering the signal                  ----------#

ift(deblured_signal,recovered_signal) # taking IFT of deblured_signal and storing result in recovered_signal

# recovered_signal is the output of question 1

# plt.plot(time_axis,signal_x)
# plt.plot(time_axis,recovered_signal)
# plt.plot(time_axis,dtft_of_denoised_signal)
# plt.plot(time_axis,signal_x,'r')
# plt.show()



#-----------------                question2            ------------------------#

dtft(signal_y,dtft_of_signal_y)  # takeing dtft of signal_y and storing it in dtft_of_signal_y
deblured_signal_q2 =[]
denoised_signal_q2 = []  # answer of question 2
recovered_signal_q2=[]
for i in range(len(dtft_of_denoised_signal)):  # dividing the dtft of y[n] and impulse response
    div =0
    div = (dtft_of_signal_y[i]) / dtft_of_impulse_response[i]
    deblured_signal_q2.append(div)
ift(deblured_signal_q2,recovered_signal_q2)  # taking IFT of deblured_signal
def denoise(signal):           # denoising the deblured_signal
    for n in range(193):
        sum = 0
        for k in range(193):
            sum+= signal[k]*array(n - k)
        denoised_signal_q2.append(sum)
denoise(recovered_signal_q2)   # calling the denoise function

'''
#-------------            error calculation                           ---------#

error1=[]
error2=[]
for i in range(193):
    k=0
    k+=signal_x[i]-recovered_signal[i]
    error1.append(k)
for i in range(193):
    p=0
    p+=signal_x[i]-recovered_signal_q2[i]
    error2.append(p)
percenatge_error1=[]
percenatge_error2=[]
a=0
b=0
for i in range(193):
    a+=error1[i]
    b+=error2[i]
percenatge_error1=abs(a/193)*100
percenatge_error2=abs(b/193)*100
print(percenatge_error1)
print(percenatge_error2)

# plt.title('Error 1')
# plt.plot(time_axis,error1 ,'orange')
# plt.show()
# plt.title('Error 2')
# plt.plot(time_axis,error2,'orange')
# plt.show()
'''
