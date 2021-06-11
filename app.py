

from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model

from tensorflow.keras.preprocessing import image
import h5py
import tensorflow as tf


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()

MODEL_PATH ='bird-96test'

# Load your trained model


model = load_model(MODEL_PATH)





def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224,3))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x = np.expand_dims(x, axis=0)
   

   

    preds = model.predict(x)
    preds=np.argmax(preds,axis =-1)
    
    classes = {"0": "AFRICAN CROWNED CRANE", "1": "AFRICAN FIREFINCH", "2": "ALBATROSS", "3": "ALEXANDRINE PARAKEET", "4": "AMERICAN AVOCET", "5": "AMERICAN BITTERN", "6": "AMERICAN COOT", "7": "AMERICAN GOLDFINCH", "8": "AMERICAN KESTREL", "9": "AMERICAN PIPIT", "10": "AMERICAN REDSTART", "11": "ANHINGA", "12": "ANNAS HUMMINGBIRD", "13": "ANTBIRD", "14": "ARARIPE MANAKIN", "15": "ASIAN CRESTED IBIS", "16": "BALD EAGLE", "17": "BALI STARLING", "18": "BALTIMORE ORIOLE", "19": "BANANAQUIT", "20": "BANDED BROADBILL", "21": "BAR-TAILED GODWIT", "22": "BARN OWL", "23": "BARN SWALLOW", "24": "BARRED PUFFBIRD", "25": "BAY-BREASTED WARBLER", "26": "BEARDED BARBET", "27": "BEARDED REEDLING", "28": "BELTED KINGFISHER", "29": "BIRD OF PARADISE", "30": "BLACK & YELLOW bROADBILL", "31": "BLACK FRANCOLIN", "32": "BLACK SKIMMER", "33": "BLACK SWAN", "34": "BLACK TAIL CRAKE", "35": "BLACK THROATED BUSHTIT", "36": "BLACK THROATED WARBLER", "37": "BLACK VULTURE", "38": "BLACK-CAPPED CHICKADEE", "39": "BLACK-NECKED GREBE", "40": "BLACK-THROATED SPARROW", "41": "BLACKBURNIAM WARBLER", "42": "BLUE GROUSE", "43": "BLUE HERON", "44": "BOBOLINK", "45": "BORNEAN BRISTLEHEAD", "46": "BORNEAN LEAFBIRD", "47": "BROWN NOODY", "48": "BROWN THRASHER", "49": "BULWERS PHEASANT", "50": "CACTUS WREN", "51": "CALIFORNIA CONDOR", "52": "CALIFORNIA GULL", "53": "CALIFORNIA QUAIL", "54": "CANARY", "55": "CAPE MAY WARBLER", "56": "CAPUCHINBIRD", "57": "CARMINE BEE-EATER", "58": "CASPIAN TERN", "59": "CASSOWARY", "60": "CEDAR WAXWING", "61": "CHARA DE COLLAR", "62": "CHIPPING SPARROW", "63": "CHUKAR PARTRIDGE", "64": "CINNAMON TEAL", "65": "CLARKS NUTCRACKER", "66": "COCK OF THE  ROCK", "67": "COCKATOO", "68": "COMMON FIRECREST", "69": "COMMON GRACKLE", "70": "COMMON HOUSE MARTIN", "71": "COMMON LOON", "72": "COMMON POORWILL", "73": "COMMON STARLING", "74": "COUCHS KINGBIRD", "75": "CRESTED AUKLET", "76": "CRESTED CARACARA", "77": "CRESTED NUTHATCH", "78": "CROW", "79": "CROWNED PIGEON", "80": "CUBAN TODY", "81": "CURL CRESTED ARACURI", "82": "D-ARNAUDS BARBET", "83": "DARK EYED JUNCO", "84": "DOUBLE BARRED FINCH", "85": "DOWNY WOODPECKER", "86": "EASTERN BLUEBIRD", "87": "EASTERN MEADOWLARK", "88": "EASTERN ROSELLA", "89": "EASTERN TOWEE", "90": "ELEGANT TROGON", "91": "ELLIOTS  PHEASANT", "92": "EMPEROR PENGUIN", "93": "EMU", "94": "ENGGANO MYNA", "95": "EURASIAN GOLDEN ORIOLE", "96": "EURASIAN MAGPIE", "97": "EVENING GROSBEAK", "98": "FIRE TAILLED MYZORNIS", "99": "FLAME TANAGER", "100": "FLAMINGO", "101": "FRIGATE", "102": "GAMBELS QUAIL", "103": "GANG GANG COCKATOO", "104": "GILA WOODPECKER", "105": "GILDED FLICKER", "106": "GLOSSY IBIS", "107": "GO AWAY BIRD", "108": "GOLD WING WARBLER", "109": "GOLDEN CHEEKED WARBLER", "110": "GOLDEN CHLOROPHONIA", "111": "GOLDEN EAGLE", "112": "GOLDEN PHEASANT", "113": "GOLDEN PIPIT", "114": "GOULDIAN FINCH", "115": "GRAY CATBIRD", "116": "GRAY PARTRIDGE", "117": "GREAT POTOO", "118": "GREATOR SAGE GROUSE", "119": "GREEN JAY", "120": "GREEN MAGPIE", "121": "GREY PLOVER", "122": "GUINEA TURACO", "123": "GUINEAFOWL", "124": "GYRFALCON", "125": "HARPY EAGLE", "126": "HAWAIIAN GOOSE", "127": "HELMET VANGA", "128": "HIMALAYAN MONAL", "129": "HOATZIN", "130": "HOODED MERGANSER", "131": "HOOPOES", "132": "HORNBILL", "133": "HORNED GUAN", "134": "HORNED SUNGEM", "135": "HOUSE FINCH", "136": "HOUSE SPARROW", "137": "IMPERIAL SHAQ", "138": "INCA TERN", "139": "INDIAN BUSTARD", "140": "INDIAN PITTA", "141": "INDIGO BUNTING", "142": "JABIRU", "143": "JAVA SPARROW", "144": "KAKAPO", "145": "KILLDEAR", "146": "KING VULTURE", "147": "KIWI", "148": "KOOKABURRA", "149": "LARK BUNTING", "150": "LEARS MACAW", "151": "LILAC ROLLER", "152": "LONG-EARED OWL", "153": "MAGPIE GOOSE", "154": "MALABAR HORNBILL", "155": "MALACHITE KINGFISHER", "156": "MALEO", "157": "MALLARD DUCK", "158": "MANDRIN DUCK", "159": "MARABOU STORK", "160": "MASKED BOOBY", "161": "MASKED LAPWING", "162": "MIKADO  PHEASANT", "163": "MOURNING DOVE", "164": "MYNA", "165": "NICOBAR PIGEON", "166": "NOISY FRIARBIRD", "167": "NORTHERN BALD IBIS", "168": "NORTHERN CARDINAL", "169": "NORTHERN FLICKER", "170": "NORTHERN GANNET", "171": "NORTHERN GOSHAWK", "172": "NORTHERN JACANA", "173": "NORTHERN MOCKINGBIRD", "174": "NORTHERN PARULA", "175": "NORTHERN RED BISHOP", "176": "NORTHERN SHOVELER", "177": "OCELLATED TURKEY", "178": "OKINAWA RAIL", "179": "OSPREY", "180": "OSTRICH", "181": "OVENBIRD", "182": "OYSTER CATCHER", "183": "PAINTED BUNTIG", "184": "PALILA", "185": "PARADISE TANAGER", "186": "PARAKETT  AKULET", "187": "PARUS MAJOR", "188": "PEACOCK", "189": "PELICAN", "190": "PEREGRINE FALCON", "191": "PHILIPPINE EAGLE", "192": "PINK ROBIN", "193": "PUFFIN", "194": "PURPLE FINCH", "195": "PURPLE GALLINULE", "196": "PURPLE MARTIN", "197": "PURPLE SWAMPHEN", "198": "PYGMY KINGFISHER", "199": "QUETZAL", "200": "RAINBOW LORIKEET", "201": "RAZORBILL", "202": "RED BEARDED BEE EATER", "203": "RED BELLIED PITTA", "204": "RED BROWED FINCH", "205": "RED FACED CORMORANT", "206": "RED FACED WARBLER", "207": "RED HEADED DUCK", "208": "RED HEADED WOODPECKER", "209": "RED HONEY CREEPER", "210": "RED TAILED THRUSH", "211": "RED WINGED BLACKBIRD", "212": "RED WISKERED BULBUL", "213": "REGENT BOWERBIRD", "214": "RING-NECKED PHEASANT", "215": "ROADRUNNER", "216": "ROBIN", "217": "ROCK DOVE", "218": "ROSY FACED LOVEBIRD", "219": "ROUGH LEG BUZZARD", "220": "ROYAL FLYCATCHER", "221": "RUBY THROATED HUMMINGBIRD", "222": "RUFOUS KINGFISHER", "223": "RUFUOS MOTMOT", "224": "SAMATRAN THRUSH", "225": "SAND MARTIN", "226": "SCARLET IBIS", "227": "SCARLET MACAW", "228": "SHOEBILL", "229": "SHORT BILLED DOWITCHER", "230": "SMITHS LONGSPUR", "231": "SNOWY EGRET", "232": "SNOWY OWL", "233": "SORA", "234": "SPANGLED COTINGA", "235": "SPLENDID WREN", "236": "SPOON BILED SANDPIPER", "237": "SPOONBILL", "238": "SRI LANKA BLUE MAGPIE", "239": "STEAMER DUCK", "240": "STORK BILLED KINGFISHER", "241": "STRAWBERRY FINCH", "242": "STRIPPED SWALLOW", "243": "SUPERB STARLING", "244": "SWINHOES PHEASANT", "245": "TAIWAN MAGPIE", "246": "TAKAHE", "247": "TASMANIAN HEN", "248": "TEAL DUCK", "249": "TIT MOUSE", "250": "TOUCHAN", "251": "TOWNSENDS WARBLER", "252": "TREE SWALLOW", "253": "TRUMPTER SWAN", "254": "TURKEY VULTURE", "255": "TURQUOISE MOTMOT", "256": "UMBRELLA BIRD", "257": "VARIED THRUSH", "258": "VENEZUELIAN TROUPIAL", "259": "VERMILION FLYCATHER", "260": "VICTORIA CROWNED PIGEON", "261": "VIOLET GREEN SWALLOW", "262": "VULTURINE GUINEAFOWL", "263": "WATTLED CURASSOW", "264": "WHIMBREL", "265": "WHITE CHEEKED TURACO", "266": "WHITE NECKED RAVEN", "267": "WHITE TAILED TROPIC", "268": "WHITE THROATED BEE EATER", "269": "WILD TURKEY", "270": "WILSONS BIRD OF PARADISE", "271": "WOOD DUCK", "272": "YELLOW BELLIED FLOWERPECKER", "273": "YELLOW CACIQUE", "274": "YELLOW HEADED BLACKBIRD"}
    classes = {int(k):str(v) for k,v in classes.items()}

    
    return classes[int(preds)]


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()
