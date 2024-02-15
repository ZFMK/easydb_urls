json_template = {
	#"limit": 1000,
	#"offset": 1,
	"search": [
		{
			"type": "match",
			"mode": "token",
			"string": "2",
			"phrase": False,
			"bool": "should",
			"field": ["original_filename" ,"original_filename_basename", "_nested:objekte__organismen.sammlungsnummer", "_system_object_id"]
		},
		{
			"type": "match",
			"bool": "should",
			"mode": "token",
			"string": "2",
			"phrase": False,
			"field": ["_nested:objekte__organismen.lk_taxonnames_id._standard.text"]
		}],
	"filename": [
		{
			"type": "match",
			"bool": "must",
			"mode": "token",
			#"string": "2",
			"phrase": False,
			"field": ["original_filename"],
			"limit": 1
		}],
	"iiif": [
		{"type":"in","bool":"must","in":'',"fields":["_tags._id"]}]
}
