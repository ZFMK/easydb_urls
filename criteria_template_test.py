json_template = {
	#"limit": 1000,
	#"offset": 1,
	"search": [
		{
			"objecttypes": ["objekte", ],
			"type": "match",
			"mode": "token",
			"string": "2",
			"phrase": False,
			"bool": "should",
			"name": "datei",
			"field": ["original_filename" ,"original_filename_basename", "_nested:objekte__organismen.sammlungsnummer", "_system_object_id"]
		}
	],
	"filename": [
		{
			"type": "match",
			"bool": "must",
			"mode": "token",
			#"string": "2",
			"phrase": False,
			"fields": ["original_filename"],
			"limit": 1
		}],
	"iiif": [
		{"type":"in","bool":"must","in":'',"fields":["_tags._id"]}]
}
