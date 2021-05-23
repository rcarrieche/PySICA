
import json
import pysica



ps = pysica.Pysica()

print("Tags para carregar")
tags_vali = ['PI1980A', 'PI1981A']
# inicio = datetime.datetime("2020-11-14 00:00:00")
inicio = "2020-11-14 00:00:00"
fim = "2020-11-16 00:00:00"
planilha_vali = ps.create_dataset_vali(tags_vali, inicio, fim, 'Pressão medida nas descargas das CW, 1 mês de reconciliação')

#print(json.dumps(.__dict__, indent=2, sort_keys=True, default=str))
#print(type(planilha_vali))
#print(planilha_vali)

