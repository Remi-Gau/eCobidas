from nested_lookup import nested_lookup
import requests
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)

# map mindlogger db schema keys to schema-standards
schemaMap = {
	"_id": "@id",
	"_modelType": "@type",
	"description": "schema:description",
	"meta.abbreviation": "skos:altLabel",
	"meta.description": "skos:prefLabel"
}

mindloggerapiUrl = 'https://api.mindlogger.info/api/v1'
urlEMAPhysicalHealth = mindloggerapiUrl+ '/folder/5bd88558336da80de9145b76'

form_schema = requests.get(urlEMAPhysicalHealth).json()
meta_form_info = nested_lookup(key='meta', document=form_schema)
form_dict = {
	"@context": [
		"https://raw.githubusercontent.com/ReproNim/schema-standardization/master/contexts/generic.jsonld"
		],
	"schema:schemaVersion": "0.0.1",
	"schema:version": "0.0.1"
}
ui_list = ['screens', 'notification', 'permission', 'resumeMode']

for key, value in form_schema.items():
	if key in schemaMap:
		mapped_key = schemaMap[key]
		if (mapped_key == '@type') and (value == 'folder'):
			value = "https://raw.githubusercontent.com/ReproNim/schema-standardization/master/schemas/Activity.jsonld"
		form_dict[mapped_key] = value


def get_item_ids(ui_item):
	value_list = []
	for x in ui_item:
		value_list.append(x['@id'])
	return value_list


for key, value in meta_form_info[0].items():
	if ('meta.' + key) in schemaMap:
		mapped_key = schemaMap['meta.' + key]
	elif key in schemaMap:
		mapped_key = schemaMap[key]
	elif key in ui_list:
		mapped_key = 'ui'
		if key == 'screens':
			value = get_item_ids(value)
			key = 'order'
		value = {key: value}
	else:
		mapped_key = key
	if mapped_key in form_dict:
		form_dict[mapped_key].update(value)
	else:
		form_dict[mapped_key] = value

form_name = form_dict['skos:altLabel']
form_name = ''.join(x for x in form_name.title() if not x.isspace())
print (form_name)
with open(form_name + '.jsonld', 'w') as fp:
	json.dump(form_dict, fp, indent=4)

itemMap = {
	"_id": "@id",
	"description": "schema:description",
	"text": "question"
}
item_ui = {
			'skipToScreen': 'skipTo',
			'skippable': 'requiredValue',
			'surveyType': 'inputType'
		}
resp_items = {
	'mode': 'multipleChoice',
	'options': 'choices',
	'optionsCount': 'count',
	'optionsMax': 'maxValue',
	'optionsMin': 'minValue'
}


for item in form_schema['meta']['screens']:
	itemUrl = mindloggerapiUrl + '/' + item['@id']
	item_schema = requests.get(itemUrl).json() # each item schema
	item_dict = {
		'@context': [
			"https://raw.githubusercontent.com/ReproNim/schema-standardization/master/contexts/generic.jsonld"],
		'@type': "https://raw.githubusercontent.com/ReproNim/schema-standardization/master/schemas/Field.jsonld",
		"schema:schemaVersion": "0.0.1",
		"schema:version": "0.0.1",
	}
	for key, value in item_schema.items():
		if key in itemMap:
			mapped_key = itemMap[key]
			val = value
			item_dict[mapped_key] = value
		elif key == 'meta':
			for k, v in value.items():
				val = v
				if k in itemMap:
					mapped_key = itemMap[k]
					val = v
				elif k in item_ui.keys():
					mapped_key = 'ui'
					if k == 'surveyType' and v == 'list':
						v = 'radio'
					val = {item_ui[k]: v}
				elif k == 'survey':
					mapped_key = 'responseOptions'
					resp = {}
					for ky, vl in v.items():
						if ky in resp_items.keys():
							rk = resp_items[ky]
							if ky == 'mode':  # MCQ
								if vl == 'single':
									vl = 'false'  # one answer question
								else:
									vl = 'true'  # multiple choice options
							if ky == 'options':
								new_vl = []
								for c in vl:
									new_vl.append({'schema:name': c['text']})
								vl = new_vl
							resp.update({rk: vl})
					val = resp
				else:
					mapped_key = k
					val = v
				if mapped_key in item_dict:
					item_dict[mapped_key].update(val)
				else:
					item_dict[mapped_key] = val

	with open(item_schema['_id'] + '_schema.jsonld', 'w') as fp:
		json.dump(item_dict, fp, indent=4)
