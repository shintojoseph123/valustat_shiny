

from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from . import plots

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from math import sqrt
import numpy as np
import json
from django.template import loader,Context
from django.http import JsonResponse
from django.template import Context




class IndexView(TemplateView):
    template_name = "index.html"

@csrf_exempt
def plotly_ajax(request):

    if request.POST:

        response_data={}

        start_capital = request.POST['capital']
        monthly_withdrawls =request.POST['monthly_return']
        n_ob = request.POST['n_ob']
        annual_mean_return = request.POST['return']
        annual_ret_std_dev = request.POST['investment_volatility']
        annual_inflation = request.POST['inflation']
        annual_inflation_std_dev = request.POST['inflation_volatility']
        n_sim = request.POST['n_sim']
        value_in_future = request.POST['future_value']
        # value_in_years = request.POST['future_year']


        start_capital = int(start_capital)
        monthly_withdrawls = int(monthly_withdrawls)
        n_ob = int(n_ob)
        annual_mean_return = int(annual_mean_return)
        annual_ret_std_dev = int(annual_ret_std_dev)
        annual_inflation = int(annual_inflation)
        annual_inflation_std_dev = int(annual_inflation_std_dev)
        n_sim = int(n_sim)
        value_in_future = int(value_in_future)






# input


        start_capital = start_capital
        monthly_withdrawls = monthly_withdrawls

        n_ob = n_ob
        n_sim = n_sim

        annual_mean_return = int(annual_mean_return)
        annual_mean_return = annual_mean_return/float(100)
        annual_ret_std_dev = annual_ret_std_dev/float(100)
        annual_inflation = annual_inflation/float(100)
        annual_inflation_std_dev = annual_inflation_std_dev/float(100)

        value_in_future = value_in_future
        value_in_years = n_ob



        value_in_future = value_in_future/float(1000000)
        value_in_years = value_in_years*12



# starting simulation

        n_ob = 12*n_ob

        monthly_mean_return = annual_mean_return/12
        monthly_ret_std_dev = annual_ret_std_dev/sqrt(12)

        monthly_inflation = annual_inflation/12
        monthly_inflation_std_dev = annual_inflation_std_dev/sqrt(12)

        monthly_investment_returns = np.zeros((n_ob, n_sim))
        monthly_inflation_returns = np.zeros((n_ob, n_sim))

# calculating random normal variables

        a = np.random.normal(loc = monthly_mean_return, scale = monthly_ret_std_dev, size = n_sim*n_ob)
        b = np.random.normal(loc = monthly_inflation, scale = monthly_inflation_std_dev, size = n_sim*n_ob)


        k = 0
        for i in range(0,n_ob):
            for j in range(0,n_sim):
                monthly_investment_returns[i,j] = a[k]
                monthly_inflation_returns[i,j] = b[k]
                k = k+1

# calculating nav matrix

        nav = np.full((n_ob+1,n_sim),start_capital)


        for i in range(0,n_ob):
            for j in range(0,n_sim):
                nav[i+1,j] = nav[i,j]*((monthly_investment_returns[i,j]-monthly_inflation_returns[i,j])+1)-monthly_withdrawls

        nav[[nav<0]] = 0

        nav = nav/1000000

        shap = nav.shape
        row = shap[0]
        column = shap[1]


# calculating probability

        future = nav[value_in_years]

        probability = 0

        for i in range(n_sim):
            if future[i] >= value_in_future:
                probability = probability+1

        prob_percent = (probability*100)/n_sim

        extra = (prob_percent*4)/5
        out = prob_percent+extra

# calculating percentage table

        row_five = []
        n = 60
        for i  in range(row+1):
            if n <= (row+1):
                row_five.append(n)
                n = n + 60


        five_array = []

        for m in row_five:
            got_row = nav[m]

            got_row = sorted(got_row)

            five_array.append(got_row)



        eighty = int(n_sim * (80/float(100)))
        sixty = int(n_sim * (60/float(100)))
        fourty = int(n_sim * (40/float(100)))
        twenty = int(n_sim * (20/float(100)))
        five = int(n_sim * (5/float(100)))

        percent = [eighty,sixty,fourty,twenty,five]

        percent_array = []

        for h in five_array:
            l = []
            for m in percent:
                l.append(h[m])

            percent_array.append(l)



        years = []

        for i in row_five:
            i = i/12
            years.append(i)

        string = " years"


        string_years = ['percentile']

        for i in years:
            i = str(i)
            i = i + string
            string_years.append(i)



        years = string_years

        percent_array = np.array(percent_array)

        mat = [years]

        col = 0

        if not len(percent_array)==0:

            ro = len(percent_array)
            col = len(percent_array[0])


            for i in range(col):
                sel = []
                for j in range(ro):
                    sel.append(percent_array[j,i])
                mat.append(sel)
        else:
            print " "



# plotting percent table

        percent_table = plots.table(percent_array,years)

# plotting percent graph

        if not col == 0:
            percent_graph = plots.tabe_graph(mat,years,col)
        else:
            percent_graph = 0







# plotting spline graph

        x_axis = []
        for k in range(n_ob+1):
            x_axis.append(k)

        loop = {}

        for i in range(0,column):
            loop[i] = []
            for j in range(0,row):
                loop[i].append(nav[j,i])

# calculating spline percent

        spline_column = nav[row-1]

        spline_column = sorted(spline_column)


        spline_percent = []
        for m in percent:
            spline_percent.append(spline_column[m])

        final_row = len(loop[0])-1

        spline_graph = plots.spline(x_axis,loop,column,spline_percent,final_row)


        data = json.dumps({'prob_percent':prob_percent,'out':out,'percent_table':percent_table,'percent_graph':percent_graph,'spline_graph':spline_graph})

        return HttpResponse(data, content_type='application/json')



    return render(request, 'index.html', {})
