import json, re
nb = json.load(open(r"notebooks\kaggle_pipeline.ipynb", encoding="utf-8"))
print("cells:", len(nb["cells"]))
for i, c in enumerate(nb["cells"]):
    src = "".join(c["source"])
    if c["cell_type"] == "markdown":
        print("--- [%d] MD ---" % i)
        print(src[:800])
    else:
        print("--- [%d] CODE (%d lines) ---" % (i, len(src.splitlines())))
        print(src[:2500])
