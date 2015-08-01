from weensylolking import app
from flask import render_template, request
from RiotAPI import RiotAPI
from .forms import InputForm
import Consts as Consts


@app.route('/', methods=['GET', 'POST'])
def index_post():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        api = RiotAPI(Consts.DEVKEY)

        input_text = form.openid.data
	input_text = input_text.lower()
        processed_text = input_text.replace(" ", "")

        summonername = {'name': processed_text}
        apicall = api.get_summoner_by_name(summonername['name'])
        if apicall[0] != 200:
            error = apicall[0]
            if error == 404:
                msg = "Summoner does not exist!"
            else:
                msg = "Error " + str(error) + ". Oops!"
            return render_template("index_error.html", form=form, error=msg)

        summonerdata = apicall[1]

	summonerlevel = summonerdata[summonername['name']]['summonerLevel']

        summonerid = summonerdata[summonername['name']]['id']

        summonerrank = api.get_summoner_rank(summonerid)[1]

        outputname = summonerdata[summonername['name']]['name']

	if summonerlevel < 30:
		msg = "Summoner is not level 30 yet!"
		return render_template("index_error.html", form=form, error=msg)

	if summonerrank == 0:
		msg = "Summoner is unranked!"
		return render_template("index_error.html", form=form, error=msg)

        outputtier = summonerrank[str(summonerid)][0]['tier']
        outputdivision = summonerrank[str(summonerid)][0]['entries'][0]['division']
        outputlp = str(summonerrank[str(summonerid)][0]['entries'][0]['leaguePoints'])

        return render_template("index.html", form=form, name=outputname, tier=outputtier,
                               division=outputdivision, lp=outputlp)

    else:
        return render_template("index_blank.html", form=form)

