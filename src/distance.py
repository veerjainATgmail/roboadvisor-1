def initialize(context):
    print ("Starting the robo advisor")

    config = ConfigParser()
    core_series = symbols('VTI', 'VXUS', 'BND', 'BNDX')
    crsp_series = symbols('VUG', 'VTV', 'VB', 'VEA', 'VWO', 'BSV', 'BIV', 'BLV', 'VMBS', 'BNDX')
    sp_series = symbols('VOO', 'VXF', 'VEA', 'VWO', 'BSV', 'BIV', 'BLV', 'VMBS', 'BNDX')
    russell_series = symbols('VONG', 'VONV', 'VTWO', 'VEA', 'VTWO', 'VEA', 'VWO', 'BSV', 'BIV', 'BLV', 'VMBS', 'BNDX')
    income_series = symbols('VTI', 'VYM', 'VXUS', 'VYMI', 'BND', 'VTC', 'BNDX')
    tax_series = symbols('VUG', 'VTV', 'VB', 'VEA', 'VWO', 'VTEB')

    context.stocks = crsp_series
    risk_based_allocation = section_to_dict('CRSP_SERIES', config)
    #1-9 for Tax Efficient Series, 0-10 otherwise
    risk_level = 5
    if (risk_level not in risk_based_allocation):
        raise Exception("Portfolio Doesn't Have Risk Level")
    context.target_allocation = dict(zip(context.stocks, risk_based_allocation[risk_level]))
    context.bought = False

    schedule_function(
    func=before_trading_starts,
    date_rule=date_rules.every_day(),
    time_rule=time_rules.market_open(hours=1),
    )


def handle_data(context, data):
    if (context.bought == False):
        print("Buying for the first time!")
        for stock in context.stocks:
            if (context.target_allocation[stock] == 0):
                continue
            amount = (context.target_allocation[stock] * context.portfolio.cash) / data.current(stock, 'price')
            order(stock, int(amount))
            print("Buying " + str(int(amount)) + " shares of " + str(stock))
        context.bought = True


def before_trading_starts(context, data):
    #total value of portfolio
    value = context.portfolio.portfolio_value
    #calculating current weights for each position
    for stock in context.stocks:
        if (context.target_allocation[stock] == 0):
            continue
        current_holdings = data.current(stock,'close') * context.portfolio.positions[stock].amount
        weight = current_holdings/value
        growth = float(weight) / float(context.target_allocation[stock])
        #if weights of any position exceed threshold, trigger rebalance
        if (growth >= 1.05 or growth <= 0.95)
            print("Need to rebalance portfolio!")
            break
    print("No need to rebalance!")

def section_to_dict(section, parser):
    parser.read('/home/robo-advisor/src/universe-config.ini')
    out_dict = {}
    for key in config[section]:
        out_dict[int(key)] = ast.literal_eval(parser[section][key])
    return(out_dict)
