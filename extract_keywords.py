import re
import os
import csv
from collections import defaultdict

# 200 Macroeconomics & THANK/HANK keywords with expected Japanese translations
keywords_dict = {
    "Heterogeneous Agent": ["異質的エージェント", "異質な主体", "異質的主体"],
    "New Keynesian": ["ニューケインジアン"],
    "Representative Agent": ["代表的エージェント", "代表的個人"],
    "HANK": ["HANK"],
    "TANK": ["TANK"],
    "RANK": ["RANK"],
    "THANK": ["THANK"],
    "hand-to-mouth": ["手元消費", "その日暮らし", "ハンド・トゥ・マウス"],
    "saver": ["貯蓄者"],
    "marginal propensity to consume": ["限界消費性向"],
    "MPC": ["MPC"],
    "intertemporal marginal propensity to consume": ["異時点間限界消費性向"],
    "iMPC": ["iMPC"],
    "precautionary savings": ["予備的貯蓄"],
    "precautionary motive": ["予備的動機"],
    "liquidity constraint": ["流動性制約"],
    "borrowing constraint": ["借入制約", "借入不可条件"],
    "idiosyncratic risk": ["固有リスク", "特異的リスク"],
    "uninsurable risk": ["保険不可能なリスク"],
    "aggregate shock": ["集計ショック", "マクロショック"],
    "business cycle": ["景気循環"],
    "steady state": ["定常状態"],
    "Euler equation": ["オイラー方程式"],
    "budget constraint": ["予算制約"],
    "utility function": ["効用関数"],
    "discount factor": ["割引因子", "割引率"],
    "risk aversion": ["リスク回避度", "リスク回避"],
    "elasticity of substitution": ["代替弾力性"],
    "Frisch elasticity": ["フリッシュ弾力性"],
    "labor supply": ["労働供給"],
    "consumption": ["消費"],
    "investment": ["投資"],
    "output": ["産出", "生産"],
    "income": ["所得"],
    "wealth": ["資産", "富"],
    "inequality": ["不平等", "格差"],
    "cyclical inequality": ["循環的不平等"],
    "monetary policy": ["金融政策"],
    "fiscal policy": ["財政政策"],
    "Taylor rule": ["テイラー・ルール", "テーラー・ルール"],
    "forward guidance": ["フォワード・ガイダンス"],
    "forward guidance puzzle": ["フォワード・ガイダンス・パズル"],
    "Catch-22": ["キャッチ22"],
    "divine coincidence": ["神の再一致"],
    "inflation": ["インフレ", "インフレーション"],
    "deflation": ["デフレ", "デフレーション"],
    "interest rate": ["利子率", "金利"],
    "nominal interest rate": ["名目利子率"],
    "real interest rate": ["実質利子率"],
    "wage": ["賃金"],
    "real wage": ["実質賃金"],
    "profit": ["利潤"],
    "dividend": ["配当"],
    "taxes": ["税", "税金", "租税"],
    "transfers": ["移転", "移転支出"],
    "government debt": ["政府債務", "公的債務"],
    "government bonds": ["政府債券", "国債"],
    "bonds": ["債券"],
    "liquidity": ["流動性"],
    "illiquid assets": ["非流動的資産"],
    "liquid assets": ["流動的資産"],
    "portfolio": ["ポートフォリオ"],
    "central bank": ["中央銀行"],
    "fiscal authority": ["財政当局"],
    "Wicksellian": ["ヴィクセル的", "ウィクセル的"],
    "price level targeting": ["物価水準ターゲティング"],
    "Fiscal Theory of the Price Level": ["物価水準の財政理論"],
    "FTPL": ["FTPL"],
    "determinacy": ["決定性"],
    "indeterminacy": ["非決定性"],
    "sunspot": ["サン・スポット", "サンスポット"],
    "log-linearization": ["対数線形化"],
    "difference equation": ["差分方程式"],
    "characteristic polynomial": ["特性多項式"],
    "eigenvalue": ["固有値"],
    "master equation": ["マスター方程式"],
    "tractable": ["扱いやすい", "トラクタブル"],
    "tractability": ["扱いやすさ", "トラクタビリティ"],
    "aggregation": ["集計", "アグリゲーション"],
    "dispersion": ["分散", "ばらつき"],
    "variance": ["分散"],
    "skewness": ["歪度"],
    "countercyclical": ["反循環的"],
    "procyclical": ["順循環的"],
    "acyclical": ["非循環的"],
    "amplification": ["増幅"],
    "dampening": ["減衰", "抑制"],
    "multiplier": ["乗数"],
    "fiscal multiplier": ["財政乗数"],
    "New Keynesian Phillips Curve": ["ニューケインジアン・フィリップス曲線"],
    "NKPC": ["NKPC"],
    "IS curve": ["IS曲線"],
    "monopolistic competition": ["独占的競争"],
    "sticky prices": ["粘着価格", "価格粘着性"],
    "sticky wages": ["粘着賃金", "賃金粘着性"],
    "Calvo": ["カルヴォ", "Calvo"],
    "Rotemberg": ["ローテンバーグ", "Rotemberg"],
    "markup": ["マークアップ"],
    "marginal cost": ["限界費用"],
    "Phillips curve": ["フィリップス曲線"],
    "welfare": ["厚生"],
    "welfare loss": ["厚生損失"],
    "loss function": ["損失関数"],
    "first-best": ["ファーストベスト", "最適"],
    "second-best": ["セカンドベスト"],
    "optimal policy": ["最適政策"],
    "commitment": ["コミットメント"],
    "discretion": ["裁量"],
    "Ramsey": ["ラムゼイ"],
    "complete markets": ["完備市場", "完全市場"],
    "incomplete markets": ["不完備市場", "不完全市場"],
    "insurance": ["保険"],
    "self-insurance": ["自己保険"],
    "perfect foresight": ["完全予見"],
    "rational expectations": ["合理的期待"],
    "transition dynamics": ["移行動学", "遷移過程"],
    "state variable": ["状態変数"],
    "jump variable": ["ジャンプ変数"],
    "aggregate demand": ["集計需要", "総需要"],
    "aggregate supply": ["集計供給", "総供給"],
    "production function": ["生産関数"],
    "technology shock": ["技術ショック"],
    "monetary policy shock": ["金融政策ショック", "金融ショック"],
    "demand shock": ["需要ショック"],
    "cost-push shock": ["コストプッシュ・ショック"],
    "capital": ["資本"],
    "investment adjustment costs": ["投資調整費用"],
    "Tobin's q": ["トービンのq"],
    "user cost of capital": ["資本の使用者費用"],
    "depreciation": ["減価償却"],
    "labor market": ["労働市場"],
    "search and matching": ["サーチ・アンド・マッチング"],
    "unemployment": ["失業"],
    "unemployment risk": ["失業リスク"],
    "job finding rate": ["求職率", "就職率"],
    "separation rate": ["離職率"],
    "wage rigidity": ["賃金硬直性"],
    "real rigidities": ["実質硬直性"],
    "nominal rigidities": ["名目硬直性"],
    "strategic complementarity": ["戦略的補完性"],
    "strategic substitutability": ["戦略的代替性"],
    "menu costs": ["メニュー・コスト"],
    "zero lower bound": ["ゼロ下限", "ZLB"],
    "liquidity trap": ["流動性の罠"],
    "quantitative easing": ["量的緩和"],
    "balance sheet": ["バランスシート", "貸借対照表"],
    "credit friction": ["信用の摩擦"],
    "financial intermediary": ["金融仲介機関"],
    "financial accelerator": ["金融アクセラレーター"],
    "collateral": ["担保"],
    "leverage": ["レバレッジ"],
    "default": ["デフォルト", "債務不履行"],
    "heterogeneity": ["異質性"],
    "distribution": ["分布"],
    "wealth distribution": ["資産分布"],
    "income distribution": ["所得分布"],
    "Gini coefficient": ["ジニ係数"],
    "top 1%": ["トップ1%", "上位1%"],
    "percentile": ["パーセンタイル"],
    "transition matrix": ["推移行列", "遷移行列"],
    "Markov chain": ["マルコフ連鎖"],
    "persistence": ["持続性"],
    "volatility": ["ボラティリティ", "変動性"],
    "covariance": ["共分散"],
    "correlation": ["相関"],
    "approximation": ["近似"],
    "first-order": ["1次", "一階"],
    "second-order": ["2次", "二階"],
    "welfare criteria": ["厚生基準"],
    "utilitarian": ["功利主義的"],
    "social planner": ["社会計画者"],
    "efficiency": ["効率性"],
    "equity": ["公平性"],
    "redistribution": ["再分配"],
    "progressive taxation": ["累進課税"],
    "lump-sum tax": ["一括税"],
    "distortionary tax": ["歪み的税", "歪みをもたらす税"],
    "subsidy": ["補助金"],
    "automatic stabilizers": ["自動安定化装置", "ビルトイン・スタビライザー"],
    "rule-of-thumb": ["ルール・オブ・サム", "経験則"],
    "bounded rationality": ["限定合理性"],
    "behavioral": ["行動的"],
    "cognitive discounting": ["認知的割引"],
    "information friction": ["情報の摩擦"],
    "sticky information": ["粘着情報"],
    "rational inattention": ["合理的無関心"],
    "empirical": ["実証的"],
    "quantitative": ["定量的"],
    "calibration": ["キャリブレーション"],
    "estimation": ["推定"],
    "Bayesian": ["ベイズ的"],
    "identification": ["識別"],
    "micro data": ["ミクロデータ"],
    "macro data": ["マクロデータ"],
    "panel data": ["パネルデータ"],
    "cross-section": ["横断面", "クロスセクション"],
    "time series": ["時系列"]
}

chapters = ["1", "2", "3", "4", "5", "6", "8"]

results = []

for ch in chapters:
    en_file = f"Bilbiie/textbook-Ch{ch}.qmd"
    ja_file = f"Bilbiie/textbook-Ch{ch}-ja.qmd"
    
    if not os.path.exists(en_file) or not os.path.exists(ja_file):
        continue
        
    with open(en_file, 'r', encoding='utf-8') as f:
        en_content = f.read()
    with open(ja_file, 'r', encoding='utf-8') as f:
        ja_content = f.read()
        
    en_paras = [p.strip() for p in en_content.split('\n\n') if p.strip()]
    ja_paras = [p.strip() for p in ja_content.split('\n\n') if p.strip()]
    
    # We will just do a global search in the chapter for simplicity, 
    # but aligning paragraphs helps pinpoint the exact translation context.
    # Because alignments might not be 1:1, we'll use a sliding window or global check.
    
    # For each keyword, if it appears in English chapter, check how it is translated in Japanese chapter.
    for kw, expected_ja in keywords_dict.items():
        # Case-insensitive search for the English keyword
        pattern = re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE)
        
        # Find all English paragraphs containing the keyword
        matched_en_indices = [i for i, p in enumerate(en_paras) if pattern.search(p)]
        
        if not matched_en_indices:
            continue
            
        found_translations = set()
        missing_translation_contexts = []
        
        for idx in matched_en_indices:
            # Look at corresponding Japanese paragraph +/- 2 paragraphs to account for misalignment
            start_idx = max(0, idx - 2)
            end_idx = min(len(ja_paras), idx + 3)
            
            ja_context = " ".join(ja_paras[start_idx:end_idx])
            
            # Check which expected translations appear
            matched_any = False
            for ja_term in expected_ja:
                if ja_term in ja_context:
                    found_translations.add(ja_term)
                    matched_any = True
            
            # If no expected translation is found, try to guess or just flag it
            if not matched_any:
                missing_translation_contexts.append(ja_paras[min(idx, len(ja_paras)-1)])
                
        # Record the finding
        results.append({
            "Chapter": ch,
            "English Keyword": kw,
            "Used Translations": " | ".join(found_translations),
            "Expected but not found": " | ".join([t for t in expected_ja if t not in found_translations]),
            "Missing Context (if not in expected)": missing_translation_contexts[0][:50] + "..." if missing_translation_contexts else ""
        })

# Aggregate by Keyword across chapters
aggregated = defaultdict(set)
for r in results:
    kw = r["English Keyword"]
    used = [u for u in r["Used Translations"].split(" | ") if u]
    aggregated[kw].update(used)
    
# We want to identify terms with inconsistent translations
# Write to CSV
with open("keywords_translation_analysis.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["English Term", "Japanese Translations Used", "Notes"])
    
    count = 0
    inconsistencies = []
    
    for kw in keywords_dict.keys():
        used = aggregated[kw]
        if used:
            count += 1
            used_str = ", ".join(used)
            notes = ""
            if len(used) > 1:
                notes = "Inconsistent translation across or within chapters"
                inconsistencies.append((kw, used_str))
            writer.writerow([kw, used_str, notes])
            
    print(f"Extracted {count} keywords found in the text.")
    print("Inconsistent translations found:")
    for kw, used_str in inconsistencies:
        print(f" - {kw}: {used_str}")

