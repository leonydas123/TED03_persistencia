import csv
import json
import os
import shutil
from datetime import datetime


class GerenciadorPersistencia:

  def __init__(self, diretorio="dados"):
    self.diretorio = diretorio
    if not os.path.exists(self.diretorio):
      os.makedirs(self.diretorio)

  def _caminho(self, nome_arquivo):
    return os.path.join(self.diretorio, nome_arquivo)

  def fazer_backup(self, nome_arquivo):
    caminho_original = self._caminho(nome_arquivo)
    if os.path.exists(caminho_original):
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      nome_backup = f"backup_{timestamp}_{nome_arquivo}"
      caminho_backup = self._caminho(nome_backup)
      shutil.copy2(caminho_original, caminho_backup)
      print(f"[Backup] Backup automático realizado: {nome_backup}")

  def ler_csv(self, nome_arquivo):
    caminho = self._caminho(nome_arquivo)
    dados = []
    try:
      with open(caminho, mode="r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
          dados.append(dict(linha))
      print(f"[Sucesso] Arquivo CSV '{nome_arquivo}' lido com sucesso.")
      return dados
    except FileNotFoundError:
      print(f"[Erro] O arquivo '{nome_arquivo}' não foi encontrado.")
    except PermissionError:
      print(f"[Erro] Permissão negada para acessar '{nome_arquivo}'.")
    except UnicodeDecodeError:
      print(
          f"[Erro] Erro de codificação UTF-8 no arquivo '{nome_arquivo}'."
      )
    except Exception as e:
      print(f"[Erro Inesperado]: {e}")
    return None

  def converter_csv_para_json(self, arquivo_csv, arquivo_json):
    dados = self.ler_csv(arquivo_csv)
    if dados is not None:
      caminho_json = self._caminho(arquivo_json)
      try:
        self.fazer_backup(arquivo_json)
        with open(caminho_json, mode="w", encoding="utf-8") as arquivo:
          json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print(
            "[Sucesso] Convertido de CSV para JSON com sucesso em"
            f" '{arquivo_json}'."
        )
      except Exception as e:
        print(f"[Erro] Falha ao gravar o JSON: {e}")

  def ler_json(self, nome_arquivo):
    caminho = self._caminho(nome_arquivo)
    try:
      with open(caminho, mode="r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
      print(f"[Sucesso] Arquivo JSON '{nome_arquivo}' lido com sucesso.")
      return dados
    except FileNotFoundError:
      print(f"[Erro] O arquivo JSON '{nome_arquivo}' não foi encontrado.")
    except json.JSONDecodeError:
      print(f"[Erro] O arquivo JSON apresenta falhas de sintaxe.")
    except Exception as e:
      print(f"[Erro Inesperado]: {e}")
    return None

  def converter_json_para_csv(self, arquivo_json, arquivo_csv):
    dados = self.ler_json(arquivo_json)
    if dados:
      caminho_csv = self._caminho(arquivo_csv)
      try:
        self.fazer_backup(arquivo_csv)
        if isinstance(dados, list) and len(dados) > 0:
          chaves = dados[0].keys()
          with open(caminho_csv, mode="w", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=chaves)
            escritor.writeheader()
            escritor.writerows(dados)
          print(
              "[Sucesso] Convertido de JSON para CSV com sucesso em"
              f" '{arquivo_csv}'."
          )
        else:
          print("[Erro] Formato JSON incompatível para tabela CSV.")
      except Exception as e:
        print(f"[Erro] Falha ao gravar o CSV: {e}")


if __name__ == "__main__":
  gp = GerenciadorPersistencia()
  print("--- Módulo de Persistência Carregado com Sucesso ---")