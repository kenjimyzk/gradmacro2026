"""Generate Lecture 12 NK-cross SVGs from one common calibration.

Run from any directory: python3 scripts/lecture12/generate_nk_cross.py
No plotting library is needed. Both figures use the same scales and rate change.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "figures" / "lecture12"
BETA, GAMMA, P, LAM, CHI = .99, 1.0, 0.0, .30, 2.0
RATE_BEFORE, RATE_AFTER = -.005, -.015
X0, X1, Y0, Y1 = 130.0, 860.0, 630.0, 190.0
LIMIT = 3.0  # Percentage units on both axes.


def sx(v):
    return X0 + (X1-X0)*v/LIMIT


def sy(v):
    return Y0 - (Y0-Y1)*v/LIMIT


def text(x, y, value, css="text", extra=""):
    return f'<text class="{css}" x="{x:.4f}" y="{y:.4f}" {extra}>{escape(value)}</text>'


def line_path(css, x1, y1, x2, y2, extra=""):
    return f'<path class="{css}" d="M{x1:.6f} {y1:.6f} L{x2:.6f} {y2:.6f}" {extra}/>'


def figure(model):
    tank = model == "TANK"
    exposure = LAM*CHI if tank else 0.0
    den = 1-BETA*P*(1-exposure)
    omega = (1-BETA*(1-exposure))/den
    direct = (1-LAM if tank else 1)*BETA/(GAMMA*den)
    multiplier = direct/(1-omega)
    old_y, new_y = -100*RATE_BEFORE*multiplier, -100*RATE_AFTER*multiplier
    direct_change = 100*(RATE_BEFORE-RATE_AFTER)*direct
    total_change = new_y-old_y
    feedback_change = total_change-direct_change
    pe_before = lambda y: omega*y-100*direct*RATE_BEFORE
    pe_after = lambda y: omega*y-100*direct*RATE_AFTER
    old, bridge, new = (sx(old_y),sy(old_y)), (sx(old_y),sy(pe_after(old_y))), (sx(new_y),sy(new_y))
    color = "#25844a" if tank else "#2364a6"
    title = f"{model} の New Keynesian Cross"
    subtitle = "同じ利子率ギャップ低下：直接効果 0.70 倍、総効果 1.75 倍" if tank else "β = 0.99、p = 0：所得フィードバックは総効果の 1%"
    elements = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1220" height="810" viewBox="0 0 1220 810" role="img" aria-labelledby="title desc">
<title id="title">{title}</title>
<desc id="desc">同じ軸尺度で実質利子率ギャップをマイナス0.5からマイナス1.5パーセントポイントへ下げる比較。PEの傾きは{omega:.3f}、直接効果は{direct_change:.3f}パーセント、追加所得フィードバックは{feedback_change:.3f}パーセント、総効果は{total_change:.3f}パーセント。式から生成した図。</desc>
<metadata>beta={BETA}; gamma={GAMMA}; p={P}; lambda={LAM}; chi={CHI}; rate_before={RATE_BEFORE}; rate_after={RATE_AFTER}</metadata>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="context-stroke"/></marker>
<style>
text {{ font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Noto Sans JP", sans-serif; fill:#243241; }}
.title {{ font-size:30px; font-weight:700; }}
.subtitle {{ font-size:20px; fill:#516170; }}
.label {{ font-size:20px; font-weight:600; }}
.text {{ font-size:18px; }}
.small {{ font-size:17px; fill:#516170; }}
.value {{ font-size:27px; font-weight:700; }}
.grid {{ stroke:#dde3e8; stroke-width:1; }}
.axis {{ stroke:#516170; stroke-width:2; }}
.line45 {{ stroke:#73808e; stroke-width:2.5; fill:none; }}
.pe {{ stroke:{color}; stroke-width:3.5; fill:none; }}
.pe2 {{ stroke:{color}; stroke-width:3.5; fill:none; stroke-dasharray:10 7; }}
.direct {{ stroke:#c66a23; stroke-width:3.6; fill:none; marker-end:url(#arrow); }}
.feedback {{ stroke:#8855a6; stroke-width:3.6; fill:none; marker-end:url(#arrow); }}
.guide {{ stroke:#a6b0ba; stroke-width:1.2; stroke-dasharray:4 5; }}
</style>
</defs>
<rect width="1220" height="810" fill="white"/>
<rect x="34" y="24" width="1152" height="752" rx="16" fill="#f8fafc" stroke="#dce3e8"/>''']
    elements += [text(65,76,title,"title"),text(67,111,subtitle,"subtitle"),
                 text(67,147,"共通較正：β = 0.99、γ = 1、p = 0　｜　TANK：λ = 0.30、χ = 2","small")]
    for tick in [0,.5,1,1.5,2,2.5,3]:
        elements += [f'<line class="grid" x1="{X0}" y1="{sy(tick):.6f}" x2="{X1}" y2="{sy(tick):.6f}"/>',
                     f'<line class="grid" x1="{sx(tick):.6f}" y1="{Y1}" x2="{sx(tick):.6f}" y2="{Y0}"/>',
                     text(X0-16,sy(tick)+6,f"{tick:g}","small",'text-anchor="end"'),
                     text(sx(tick),Y0+28,f"{tick:g}","small",'text-anchor="middle"')]
    elements += [line_path("axis",X0,Y0,X1+15,Y0),line_path("axis",X0,Y0,X0,Y1-10),
                 text(122,176,"計画消費 c（%）","label"),text((X0+X1)/2,686,"現在所得 y（%）","label",'text-anchor="middle"'),
                 line_path("line45",sx(0),sy(0),sx(LIMIT),sy(LIMIT)),
                 text(731,176,"45度線 c = y","small"),
                 line_path("pe",sx(0),sy(pe_before(0)),sx(LIMIT),sy(pe_before(LIMIT))),
                 line_path("pe2",sx(0),sy(pe_after(0)),sx(LIMIT),sy(pe_after(LIMIT))),
                 line_path("direct",*old,*bridge),line_path("feedback",*bridge,*new)]
    for label,(x,y),income,shift in [("A",old,old_y,26),("B",new,new_y,-16)]:
        elements += [line_path("guide",x,y,x,Y0),f'<circle cx="{x:.6f}" cy="{y:.6f}" r="6" fill="{color}" stroke="white" stroke-width="2"/>',
                     text(x+10,y+shift,label,"label")]
    # A dedicated column keeps the one-percent RANK feedback legible without exaggerating it.
    elements += [text(917,202,"PE の傾き","small"),text(917,238,f"ω = {omega:.3f}","value"),
                 line_path("pe legend",918,277,961,277),text(974,283,"変更前","text"),
                 line_path("pe2 legend",918,311,961,311),text(974,317,"変更後","text"),
                 text(917,363,"消費・産出の増加","label"),
                 text(917,401,"直接効果","small"),text(917,435,f"{direct_change:.3f}%","value",'style="fill:#c66a23"'),
                 text(917,471,"所得フィードバック","small"),text(917,505,f"{feedback_change:.3f}%","value",'style="fill:#8855a6"'),
                 text(917,541,"総効果","small"),text(917,575,f"{total_change:.3f}%","value"),
                 text(917,616,f"A：{old_y:.3f}%","small"),text(917,645,f"B：{new_y:.3f}%","small"),
                 text(67,725,"注：両図は同じ軸尺度。変更前 r̃ = −0.5%ポイント、変更後 −1.5%ポイント（1%ポイント低下）。","small"),
                 text(67,756,"橙の矢印は所得固定のシフト、紫の矢印は新PE曲線上の移動。効果の数値は消費の縦方向の増分。","small"),"</svg>"]
    return "\n".join(elements)+"\n"


if __name__ == "__main__":
    OUT.mkdir(parents=True,exist_ok=True)
    for model in ["RANK","TANK"]:
        target=OUT/f"{model.lower()}_nk_cross.svg"
        target.write_text(figure(model))
        print(target)
