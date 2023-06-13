import math
#########################################################################################################################################################################
dict = {'strike' : 100, 'price' : 100, 'time steps' : 10, 'sigma': 0.2, 'years': 1, 'risk-free rate': 0.00, 'dividend': 0.02, 
        'callput': 1, 'AmerEu': -1}

# call = 1, put = -1; in callput
# American = 1, European = -1; in AmerEu

Prices_different_rates = []

while dict['risk-free rate'] < 4: 
    u = math.exp(dict['sigma']*math.sqrt(dict['years']/dict['time steps']))
    d = 1/u
    probup = (((math.exp((dict['risk-free rate']-dict['dividend'])*dict['years']/dict['time steps'])) - d) / (u - d))
    discount_factor = dict['risk-free rate']/dict['time steps']
    duration_of_time_step = (dict['years']/dict['time steps'])

    if dict['callput'] > 0:
        type = 'call'
    else:
        type = 'put'
    if dict['AmerEu'] > 0:
        exercise = 'American'
    else:
        exercise = 'European'
    #########################################################################################################################################################################
    def binomial():
        Tstep = dict['time steps']
        payoffs = []
        n = 0
        while n < (Tstep + 1): 
            payoffs.append(max(0, dict['callput']*(dict['price']*(u**((Tstep)-n))*(d**n) - dict['strike'])))
            n += 1
        
        while Tstep >= 1:
    #########################################################################################################################################################################
        # not used in the actual calculation but useful to see what the probabilities of each node is at a specific timestep    
            def combos(n, i):
                return math.factorial(n) / (math.factorial(n-i)*math.factorial(i))

            pascal = []
            for i in range(Tstep+1):
                pascal.append(combos(Tstep, i))

            probabilities = []
            i = 0
            for i in range(Tstep+1):
                probabilities.append(pascal[i]*(probup**((Tstep)-i))*((1-probup)**i))
                i += 1
    #########################################################################################################################################################################
            discounting1 = []
            i = 0
            while i < (Tstep):
                if dict['AmerEu'] == 1:
                    American_payoff = (dict['callput']*(dict['price']*(u**(Tstep-i-1)*(d**i)) - dict['strike']))
                    European_payoff = (((probup)*payoffs[i]) + ((1-probup)*payoffs[i+1])) / (math.exp(discount_factor))
                    discounting1.append(max(American_payoff, European_payoff))
                elif dict['AmerEu'] == -1:
                    discounting1.append((((probup)*payoffs[i]) + ((1-probup)*payoffs[i+1]))
                                        / (math.exp(discount_factor)))
                else:
                    pass
                i += 1  
                
            payoffs.clear()
            payoffs.extend(discounting1)
            
            Tstep -= 1
        return discounting1
    if binomial()[0] >= 0:
        Prices_different_rates.append(round(binomial()[0], 2))
    else:
        Prices_different_rates.append(0)
    dict['risk-free rate'] += 0.0025
    
print(Prices_different_rates)