### Table of Electric Load Curve Metrics & Indicators

+---------+---------+---------+---------+---------+---------+---------+
| In      | Type of | Meaning | Formula | Meaning | Pros &  | Sources |
| dicator | In      |         | /       | in      | Cons    |         |
|         | dicator |         | Calc    | terms   |         |         |
|         |         |         | ulation | of      |         |         |
|         |         |         |         | Energy  |         |         |
|         |         |         |         | Be      |         |         |
|         |         |         |         | haviour |         |         |
+---------+---------+---------+---------+---------+---------+---------+
| **      | Basic   | Rep     | \$L\_P  | R       | **      | Köhler  |
| Maximum | St      | resents | =       | eflects | Pros:** | et al.  |
| Value   | atistic | the     | \\fra   | the     | Es      | 2022;   |
| (Peak   | /       | **      | c{1}{n} | user-de | sential | Li et   |
| Load)** | P       | highest | \       | pendent | for     | al.     |
|         | osition | power   | \sum\_{ | active  | sizing  | 2018;   |
|         | Measure | d       | i=1}\^n | share   | grid    | Ihsane  |
|         |         | emand** | \\max   | of      | c       | et al.  |
|         |         | in the  | L\_{    | consu   | apacity | 2018;   |
|         |         | dataset | i,j}\$. | mption, | and     | B       |
|         |         | over a  |         | marking | comp    | alasubr |
|         |         | given   |         | periods | onents. | amanian |
|         |         | period. |         | of      |         | et al.  |
|         |         |         |         | simul   | **      | 2021;   |
|         |         |         |         | taneous | Cons:** | Herraiz |
|         |         |         |         | hig     | Reveals | -Cañete |
|         |         |         |         | h-power | nothing | et al.  |
|         |         |         |         | ap      | about   | 2022;   |
|         |         |         |         | pliance | cont    | Do      |
|         |         |         |         | usage.  | inuous, | minguez |
|         |         |         |         |         | passive | et al.  |
|         |         |         |         |         | base    | 2021;   |
|         |         |         |         |         | loads.  | Hart    |
|         |         |         |         |         |         | vigsson |
|         |         |         |         |         |         | &       |
|         |         |         |         |         |         | Ahlgren |
|         |         |         |         |         |         | 2018;   |
|         |         |         |         |         |         | Dickert |
|         |         |         |         |         |         | &       |
|         |         |         |         |         |         | S       |
|         |         |         |         |         |         | chegner |
|         |         |         |         |         |         | 2011;   |
|         |         |         |         |         |         | St      |
|         |         |         |         |         |         | evanato |
|         |         |         |         |         |         | et al.  |
|         |         |         |         |         |         | 2025.   |
+---------+---------+---------+---------+---------+---------+---------+
| **      | Basic   | Rep     | N/A     | In      | **      | Köhler  |
| Minimum | St      | resents |         | dicates | Pros:** | et al.  |
| Value   | atistic | the     |         | the     | Ex      | 2022;   |
| (Base   | /       | *       |         | c       | cellent | B       |
| Load)** | P       | *lowest |         | onstant | for     | alasubr |
|         | osition | power   |         | b       | iden    | amanian |
|         | Measure | d       |         | aseline | tifying | et al.  |
|         |         | emand** |         | energy  | passive | 2021;   |
|         |         | oc      |         | fo      | consu   | Li et   |
|         |         | curring |         | otprint | mption. | al.     |
|         |         | in the  |         | of      |         | 2018;   |
|         |         | d       |         | devices | **      | Hart    |
|         |         | ataset. |         | running | Cons:** | vigsson |
|         |         |         |         | 24/7    | Misses  | &       |
|         |         |         |         | (e.g.,  | dynamic | Ahlgren |
|         |         |         |         | refrige | human   | 2018.   |
|         |         |         |         | rators) | ro      |         |
|         |         |         |         | without | utines. |         |
|         |         |         |         | active  |         |         |
|         |         |         |         | human   |         |         |
|         |         |         |         | interv  |         |         |
|         |         |         |         | ention. |         |         |
+---------+---------+---------+---------+---------+---------+---------+
| **Mean  | Central | The     | \$L\_M  | Shows   | **      | Köhler  |
| Load /  | T       | **      | =       | the     | Pros:** | et al.  |
| Annual  | endency | average | \\fra   | overall | Strong  | 2022;   |
| Consum  |         | ele     | c{1}{n} | ma      | be      | B       |
| ption** |         | ctrical | \\sum   | gnitude | nchmark | alasubr |
|         |         | power   | \\left( | of      | for     | amanian |
|         |         | d       | \\frac  | demand, | co      | et al.  |
|         |         | emand** | {1}{48} | corr    | mparing | 2021;   |
|         |         | over a  | \\sum   | elating | a       | Zhang   |
|         |         | s       | L       | with    | bsolute | et al.  |
|         |         | pecific | \_{i,j} | ho      | consu   | 2022;   |
|         |         | time    | \\ri    | usehold | mption. | Li et   |
|         |         | span.   | ght)\$. | size,   |         | al.     |
|         |         |         |         | ap      | **      | 2018;   |
|         |         |         |         | pliance | Cons:** | Ihsane  |
|         |         |         |         | own     | A       | et al.  |
|         |         |         |         | ership, | verages | 2018;   |
|         |         |         |         | and     | out     | Herraiz |
|         |         |         |         | wealth. | timing, | -Cañete |
|         |         |         |         |         | vola    | et al.  |
|         |         |         |         |         | tility, | 2022;   |
|         |         |         |         |         | and     | Do      |
|         |         |         |         |         | peak    | minguez |
|         |         |         |         |         | beh     | et al.  |
|         |         |         |         |         | aviors. | 2021.   |
+---------+---------+---------+---------+---------+---------+---------+
| **R     | T       | Average | \$\\m   | Ide     | **      | Kaur et |
| elative | emporal | cons    | u\^R\_i | ntifies | Pros:** | al.     |
| Mean    | Metric  | umption | =       | s       | Nor     | 2022.   |
| Power   |         | in a    | \\mu\_i | pecific | malizes |         |
| (Bre    |         | s       | /       | t       | the     |         |
| akfast, |         | pecific | \\hat{\ | emporal | scale,  |         |
| Day,    |         | time    | \mu}\$. | habits, | f       |         |
| Dinner, |         | block   |         | easily  | ocusing |         |
| N       |         | r       |         | clas    | purely  |         |
| ight)** |         | elative |         | sifying | on      |         |
|         |         | to      |         | user    | *when*  |         |
|         |         | total   |         | r       | people  |         |
|         |         | average |         | outines | c       |         |
|         |         | consu   |         | into    | onsume. |         |
|         |         | mption. |         | s       |         |         |
|         |         |         |         | pecific | **      |         |
|         |         |         |         | active  | Cons:** |         |
|         |         |         |         | periods | O       |         |
|         |         |         |         | (e.g.,  | bscures |         |
|         |         |         |         | \"Night | the     |         |
|         |         |         |         | Consum  | a       |         |
|         |         |         |         | ers\"). | bsolute |         |
|         |         |         |         |         | peak    |         |
|         |         |         |         |         | demand  |         |
|         |         |         |         |         | mag     |         |
|         |         |         |         |         | nitudes |         |
|         |         |         |         |         | in      |         |
|         |         |         |         |         | Watts.  |         |
+---------+---------+---------+---------+---------+---------+---------+
| **Modal | Timing  | The     | \$T\_P  | D       | **      | Li et   |
| Daily   | Metric  | ha      | =       | irectly | Pros:** | al.     |
| Peak    |         | lf-hour | \\tex   | in      | Highly  | 2018.   |
| Load    |         | i       | t{mode} | dicates | useful  |         |
| Time    |         | nterval | {j      | h       | for     |         |
| (\$T\   |         | that    | \_{max} | abitual | Time    |         |
| _P\$)** |         | most    | \\L     | peak    | -of-Use |         |
|         |         | fre     | \_{i,j\ | ro      | (ToU)   |         |
|         |         | quently | _{max}} | utines, | pricing |         |
|         |         | p       | = \\max | such as | and     |         |
|         |         | roduces | L\_{i   | cooking | demand  |         |
|         |         | the     | ,j}}\$. | dinner  | re      |         |
|         |         | daily   |         | after   | sponse. |         |
|         |         | maximum |         | work or |         |         |
|         |         | load.   |         | waking  | **      |         |
|         |         |         |         | up.     | Cons:** |         |
|         |         |         |         |         | D       |         |
|         |         |         |         |         | oesn\'t |         |
|         |         |         |         |         | i       |         |
|         |         |         |         |         | ndicate |         |
|         |         |         |         |         | how     |         |
|         |         |         |         |         | intense |         |
|         |         |         |         |         | the     |         |
|         |         |         |         |         | peak    |         |
|         |         |         |         |         | is.     |         |
+---------+---------+---------+---------+---------+---------+---------+
| **Mean  | System  | Ratio   | \$L\_F  | De      | **      | Li et   |
| Daily   | /       | between | =       | scribes | Pros:** | al.     |
| Load    | Perf    | average | \\fr    | the     | C       | 2018;   |
| Factor  | ormance | load    | ac{\\te | *       | ritical | Ihsane  |
| (\$L\   |         | and     | xt{Mean | *\"peak | for     | et al.  |
| _F\$)** |         | peak    | Load    | iness\" | as      | 2018;   |
|         |         | load.   | }}{\\te | of a    | sessing | Herraiz |
|         |         |         | xt{Peak | pro     | system  | -Cañete |
|         |         |         | Load}}  | file**. | eff     | et al.  |
|         |         |         | \\times | Low     | iciency | 2022;   |
|         |         |         | 100\$.  | load    | and     | Do      |
|         |         |         |         | factors | varia   | minguez |
|         |         |         |         | mean    | bility. | et al.  |
|         |         |         |         | brief,  |         | 2021;   |
|         |         |         |         | intense | **      | Hart    |
|         |         |         |         | spikes; | Cons:** | vigsson |
|         |         |         |         | higher  | Does    | &       |
|         |         |         |         | factors | not     | Ahlgren |
|         |         |         |         | suggest | reveal  | 2018;   |
|         |         |         |         | cons    | when    | tp      |
|         |         |         |         | istent, | var     | wrs.202 |
|         |         |         |         | spr     | iations | 0.30189 |
|         |         |         |         | ead-out | occur.  | 36.pdf; |
|         |         |         |         | be      |         | St      |
|         |         |         |         | havior. |         | evanato |
|         |         |         |         |         |         | et al.  |
|         |         |         |         |         |         | 2025.   |
+---------+---------+---------+---------+---------+---------+---------+
| **C     | System  | The     | \$CF =  | Rep     | **      | Hart    |
| apacity | Metric  | f       | \\fr    | resents | Pros:** | vigsson |
| F       |         | raction | ac{\\in | how     | Primary | &       |
| actor** |         | of      | t\_0\^T | well a  | in      | Ahlgren |
|         |         | ge      | P       | system  | dicator | 2018.   |
|         |         | nerated | \_L(t)d | u       | for     |         |
|         |         | elec    | t}{P\_G | tilizes | eva     |         |
|         |         | tricity | \\cdot  | its     | luating |         |
|         |         | c       | T}\$.   | c       | the     |         |
|         |         | ompared |         | apacity | e       |         |
|         |         | to the  |         | to meet | conomic |         |
|         |         | maximum |         | agg     | vi      |         |
|         |         | p       |         | regated | ability |         |
|         |         | ossible |         | elec    | of      |         |
|         |         | gen     |         | tricity | mi      |         |
|         |         | eration |         | beh     | ni-grid |         |
|         |         | over a  |         | aviours | s       |         |
|         |         | time    |         | over    | ystems. |         |
|         |         | frame.  |         | time.   |         |         |
|         |         |         |         |         | **      |         |
|         |         |         |         |         | Cons:** |         |
|         |         |         |         |         | R       |         |
|         |         |         |         |         | equires |         |
|         |         |         |         |         | kn      |         |
|         |         |         |         |         | owledge |         |
|         |         |         |         |         | of      |         |
|         |         |         |         |         | system  |         |
|         |         |         |         |         | gen     |         |
|         |         |         |         |         | eration |         |
|         |         |         |         |         | ca      |         |
|         |         |         |         |         | pacity. |         |
+---------+---------+---------+---------+---------+---------+---------+
| **Coin  | System  | A       | \       | R       | **      | Herraiz |
| cidence | Metric  | measure | $\\frac | eflects | Pros:** | -Cañete |
| F       |         | of the  | {P\_{L, | synch   | Crucial | et al.  |
| actor** |         | lik     | Peak}}  | ronized | for     | 2022;   |
|         |         | elihood | {P\_{L, | social  | unders  | Hart    |
|         |         | that    | Tot}}\$ | ro      | tanding | vigsson |
|         |         | e       |         | utines; | the     | &       |
|         |         | lectric |         | high    | col     | Ahlgren |
|         |         | loads   |         | coin    | lective | 2018.   |
|         |         | are     |         | cidence | impact  |         |
|         |         | used    |         | means   | of      |         |
|         |         | simulta |         | oc      | be      |         |
|         |         | neously |         | cupants | haviour |         |
|         |         | by      |         | a       | on peak |         |
|         |         | con     |         | ctivate | demand  |         |
|         |         | sumers. |         | heavy   | sizing. |         |
|         |         |         |         | app     |         |         |
|         |         |         |         | liances | **      |         |
|         |         |         |         | at the  | Cons:** |         |
|         |         |         |         | exact   | R       |         |
|         |         |         |         | same    | equires |         |
|         |         |         |         | time.   | a       |         |
|         |         |         |         |         | ccurate |         |
|         |         |         |         |         | kn      |         |
|         |         |         |         |         | owledge |         |
|         |         |         |         |         | of the  |         |
|         |         |         |         |         | total   |         |
|         |         |         |         |         | in      |         |
|         |         |         |         |         | stalled |         |
|         |         |         |         |         | load of |         |
|         |         |         |         |         | all     |         |
|         |         |         |         |         | co      |         |
|         |         |         |         |         | nnected |         |
|         |         |         |         |         | appl    |         |
|         |         |         |         |         | iances. |         |
+---------+---------+---------+---------+---------+---------+---------+
| **P     | System  | The     | \$\\fr  | A       | **      | Köhler  |
| eak-to- | Metric  | ratio   | ac{\\te | higher  | Pros:** | et al.  |
| Average |         | of peak | xt{Peak | value   | Helps   | 2022.   |
| Ratio   |         | power   | Load}}{ | means   | target  |         |
| (PAR)** |         | to      | \\text{ | the ELP | cu      |         |
|         |         | average | Average | has     | stomers |         |
|         |         | consu   | L       | more    | for     |         |
|         |         | mption. | oad}}\$ | pro     | demand  |         |
|         |         |         |         | nounced | re      |         |
|         |         |         |         | power   | duction |         |
|         |         |         |         | peaks   | pr      |         |
|         |         |         |         | due to  | ograms. |         |
|         |         |         |         | agg     |         |         |
|         |         |         |         | ressive | **      |         |
|         |         |         |         | or      | Cons:** |         |
|         |         |         |         | conce   | Esse    |         |
|         |         |         |         | ntrated | ntially |         |
|         |         |         |         | ap      | the     |         |
|         |         |         |         | pliance | inverse |         |
|         |         |         |         | usage.  | of the  |         |
|         |         |         |         |         | Load    |         |
|         |         |         |         |         | Factor. |         |
+---------+---------+---------+---------+---------+---------+---------+
| **Peak  | Shape / | Cla     | Count   | Tra     | **      | Zhang   |
| Number  | Feature | ssifies | of      | nslates | Pros:** | et al.  |
| C       |         | load    | peaks   | d       | Highly  | 2022.   |
| ategory |         | p       | ex      | irectly | in      |         |
| (PNC) / |         | atterns | ceeding | to the  | tuitive |         |
| ECPk**  |         | ac      | a       | number  | for     |         |
|         |         | cording | des     | of      | li      |         |
|         |         | to      | ignated | d       | festyle |         |
|         |         | their   | thr     | istinct | segme   |         |
|         |         | number  | eshold. | in      | ntation |         |
|         |         | of      |         | tensive | and     |         |
|         |         | elec    |         | a       | clus    |         |
|         |         | tricity |         | ctivity | tering. |         |
|         |         | cons    |         | periods |         |         |
|         |         | umption |         | mapping | **      |         |
|         |         | peaks.  |         | to      | Cons:** |         |
|         |         |         |         | active  | Se      |         |
|         |         |         |         | ro      | nsitive |         |
|         |         |         |         | utines. | to the  |         |
|         |         |         |         |         | ar      |         |
|         |         |         |         |         | bitrary |         |
|         |         |         |         |         | th      |         |
|         |         |         |         |         | reshold |         |
|         |         |         |         |         | d       |         |
|         |         |         |         |         | efining |         |
|         |         |         |         |         | a       |         |
|         |         |         |         |         | \"      |         |
|         |         |         |         |         | peak\". |         |
+---------+---------+---------+---------+---------+---------+---------+
| **      | Shape / | Abs     | Finding | C       | **      | Al      |
| V-Shape | Feature | tracted | coor    | aptures | Pros:** | -Otaibi |
| &       |         | f       | dinates | the     | Signif  | et al.  |
| M-Shape |         | eatures | of      | abs     | icantly | 2016.   |
| Fea     |         | ca      | \$(T\   | tracted | reduces |         |
| tures** |         | pturing | _{max}, | ma      | dimensi |         |
|         |         | the     | C\_{    | cro-beh | onality |         |
|         |         | morning | max})\$ | avioral | c       |         |
|         |         | and     | and     | m       | ompared |         |
|         |         | evening | \$(T\   | orning/ | to raw  |         |
|         |         | peaks.  | _{min}, | evening | 24h     |         |
|         |         |         | C\_{m   | energy  | var     |         |
|         |         |         | in})\$. | r       | iables. |         |
|         |         |         |         | outines |         |         |
|         |         |         |         | over a  | **      |         |
|         |         |         |         | simple  | Cons:** |         |
|         |         |         |         | pa      | May     |         |
|         |         |         |         | rameter | miss    |         |
|         |         |         |         | set.    | an      |         |
|         |         |         |         |         | omalous |         |
|         |         |         |         |         | midday  |         |
|         |         |         |         |         | ap      |         |
|         |         |         |         |         | pliance |         |
|         |         |         |         |         | usage.  |         |
+---------+---------+---------+---------+---------+---------+---------+
| **Load  | T       | S       | Categor | Maps    | **      | B       |
| Blocks  | emporal | egments | ization | s       | Pros:** | alasubr |
| (Base,  | Categor | the 24h | by      | pecific | Very    | amanian |
| Of      | ization | curve   | h       | times   | useful  | et al.  |
| f-peak, |         | into    | our/mag | of day  | for     | 2021.   |
| Transi  |         | d       | nitude. | to      | Demand  |         |
| tional, |         | iscrete |         | in      | Side    |         |
| Sh      |         | blocks  |         | tensity | Man     |         |
| oulder, |         | based   |         | of      | agement |         |
| Interm  |         | on load |         | human   | and     |         |
| ediate, |         | ma      |         | a       | tariff  |         |
| Peak)** |         | gnitude |         | ctivity | p       |         |
|         |         | thre    |         | (e.g.,  | ricing. |         |
|         |         | sholds. |         | active  |         |         |
|         |         |         |         | cooking | **      |         |
|         |         |         |         | vs      | Cons:** |         |
|         |         |         |         | passive | Rigid   |         |
|         |         |         |         | sleep). | bou     |         |
|         |         |         |         |         | ndaries |         |
|         |         |         |         |         | might   |         |
|         |         |         |         |         | miss    |         |
|         |         |         |         |         | s       |         |
|         |         |         |         |         | hifting |         |
|         |         |         |         |         | ho      |         |
|         |         |         |         |         | usehold |         |
|         |         |         |         |         | sch     |         |
|         |         |         |         |         | edules. |         |
+---------+---------+---------+---------+---------+---------+---------+
| **Mean  | Vari    | A       | \$      | M       | **      | Kaur et |
| R       | ability | verages | \\Delta | easures | Pros:** | al.     |
| elative | Measure | the     | \\sigma | the     | C       | 2022.   |
| S       |         | r       | =       | day     | aptures |         |
| tandard |         | elative | \\fra   | -to-day | true    |         |
| De      |         | s       | c{1}{4} | vari    | beha    |         |
| viation |         | tandard | \       | ability | vioural |         |
| (       |         | de      | \sum\_{ | and     | chaos   |         |
| MRSD)** |         | viation | i=1}\^4 | irreg   | and     |         |
|         |         | across  | \\      | ularity | fluct   |         |
|         |         | di      | frac{\\ | of a    | uations |         |
|         |         | fferent | sigma\_ | c       | well.   |         |
|         |         | time    | i}{\\mu | onsumer |         |         |
|         |         | p       | \_i}\$. | (e.g.,  | **      |         |
|         |         | eriods. |         | shift   | Cons:** |         |
|         |         |         |         | wo      | Value   |         |
|         |         |         |         | rkers). | can     |         |
|         |         |         |         |         | spike   |         |
|         |         |         |         |         | artif   |         |
|         |         |         |         |         | icially |         |
|         |         |         |         |         | if the  |         |
|         |         |         |         |         | mean    |         |
|         |         |         |         |         | cons    |         |
|         |         |         |         |         | umption |         |
|         |         |         |         |         | is      |         |
|         |         |         |         |         | close   |         |
|         |         |         |         |         | to      |         |
|         |         |         |         |         | zero.   |         |
+---------+---------+---------+---------+---------+---------+---------+
| **S     | Con     | Dif     | e.g.,   | R       | **      | Kaur et |
| easonal | textual | ference | \$      | eflects | Pros:** | al.     |
| /       | Metric  | in      | WDScore | the     | I       | 2022.   |
| Weekend |         | cons    | = \\sum | impact  | solates |         |
| vs      |         | umption | \\frac{ | of      | the     |         |
| Weekday |         | between | \\\\mu\ | climate | effect  |         |
| Score** |         | seasons | _{WE,i} | changes | of work |         |
|         |         | or      | -       | or      | sc      |         |
|         |         | week    | \\mu\_  | leisur  | hedules |         |
|         |         | ends/we | {WD,i}\ | e/stay- | and     |         |
|         |         | ekdays, | \}{\\mu | at-home | climate |         |
|         |         | propo   | \_i}\$. | r       | on      |         |
|         |         | rtional |         | outines | energy  |         |
|         |         | to      |         | versus  | use.    |         |
|         |         | average |         | typical |         |         |
|         |         | demand. |         | working | **      |         |
|         |         |         |         | day     | Cons:** |         |
|         |         |         |         | habits. | R       |         |
|         |         |         |         |         | equires |         |
|         |         |         |         |         | a full  |         |
|         |         |         |         |         | year of |         |
|         |         |         |         |         | data to |         |
|         |         |         |         |         | c       |         |
|         |         |         |         |         | ompute. |         |
+---------+---------+---------+---------+---------+---------+---------+
| **      | Com     | M       | \$Ent   | In      | **      | Zhang   |
| Entropy | plexity | easures | ropy(x) | dicates | Pros:** | et al.  |
| of      | /       | the     | =       | how     | Ex      | 2022.   |
| DECP**  | Vari    | divers  | -\\sum  | regular | cellent |         |
|         | ability | ity/com | p\_c    | or      | for     |         |
|         |         | plexity | \\log(p | chaotic | unders  |         |
|         |         | of      | \_c)\$. | a       | tanding |         |
|         |         | Daily   |         | house   | the     |         |
|         |         | Elec    |         | hold\'s | com     |         |
|         |         | tricity |         | daily   | plexity |         |
|         |         | Cons    |         | r       | of      |         |
|         |         | umption |         | outines | ind     |         |
|         |         | P       |         | are.    | ividual |         |
|         |         | atterns |         | High    | li      |         |
|         |         | (DECP)  |         | entropy | festyle |         |
|         |         | within  |         | means   | sta     |         |
|         |         | a       |         | they    | bility. |         |
|         |         | d       |         | utilize |         |         |
|         |         | ataset. |         | many    | **      |         |
|         |         |         |         | di      | Cons:** |         |
|         |         |         |         | fferent | R       |         |
|         |         |         |         | pa      | equires |         |
|         |         |         |         | tterns. | pattern |         |
|         |         |         |         |         | clas    |         |
|         |         |         |         |         | sificat |         |
|         |         |         |         |         | ion/dic |         |
|         |         |         |         |         | tionary |         |
|         |         |         |         |         | b       |         |
|         |         |         |         |         | uilding |         |
|         |         |         |         |         | first.  |         |
+---------+---------+---------+---------+---------+---------+---------+
| **A     | A       | M       | \$r =   | Ide     | **      | Li et   |
| utocorr | utocorr | easures | \\      | ntifies | Pros:** | al.     |
| elation | elation | the     | frac{co | c       | Readily | 2021;   |
| /       |         | corr    | v(X\_t, | yclical | ide     | Ihsane  |
| Serial  |         | elation | X\      | be      | ntifies | et al.  |
| Corr    |         | of the  | _{t-\\t | haviors | p       | 2018.   |
| elation |         | power   | au})}{\ | or      | eriodic |         |
| Coef    |         | cons    | \sigma\ | re      | habits  |         |
| ficient |         | umption | _{X\_t} | peating | and     |         |
| (\      |         | signal  | \\sigm  | daily   | se      |         |
| $r\$)** |         | with a  | a\_{X\_ | r       | lf-simi |         |
|         |         | delayed | {t-\\ta | outines | larity. |         |
|         |         | copy of | u}}}\$. | across  |         |         |
|         |         | itself. |         | time    | **      |         |
|         |         |         |         | lags.   | Cons:** |         |
|         |         |         |         |         | Only    |         |
|         |         |         |         |         | tests   |         |
|         |         |         |         |         | for     |         |
|         |         |         |         |         | linear  |         |
|         |         |         |         |         | corre   |         |
|         |         |         |         |         | lation. |         |
+---------+---------+---------+---------+---------+---------+---------+
| **Eta   | Stat    | M       | \$\     | Det     | **      | Ihsane  |
| Corr    | istical | easures | \eta\^2 | ermines | Pros:** | et al.  |
| elation | Dep     | the     | =       | exactly | Great   | 2018.   |
| Ratio   | endency | relat   | \\      | how     | for     |         |
| (\      |         | ionship | frac{\\ | much of | quan    |         |
| $\\eta\ |         | between | sigma\_ | the     | tifying |         |
| ^2\$)** |         | dis     | {means} | va      | how     |         |
|         |         | persion | \^2}{\\ | riation | heavily |         |
|         |         | within  | sigma\_ | in      | r       |         |
|         |         | tim     | {total} | ele     | outines |         |
|         |         | e-based | \^2}\$. | ctrical | are     |         |
|         |         | demand  |         | cons    | tied to |         |
|         |         | and     |         | umption | the     |         |
|         |         | across  |         | depends | clock.  |         |
|         |         | total   |         | speci   |         |         |
|         |         | demand. |         | fically | **      |         |
|         |         |         |         | on the  | Cons:** |         |
|         |         |         |         | *time   | D       |         |
|         |         |         |         | of      | oesn\'t |         |
|         |         |         |         | day*.   | explain |         |
|         |         |         |         |         | *why*   |         |
|         |         |         |         |         | the     |         |
|         |         |         |         |         | time    |         |
|         |         |         |         |         | m       |         |
|         |         |         |         |         | atters. |         |
+---------+---------+---------+---------+---------+---------+---------+
| *       | Dis     | M       | \$Q3 -  | Defines | **      | Köhler  |
| *InterQ | persion | easures | Q1\$    | \"n     | Pros:** | et al.  |
| uartile | Measure | the     |         | ormal\" | Highly  | 2022;   |
| Range   |         | spread  |         | daily   | robust  | Zhang   |
| (IQR) / |         | of the  |         | ope     | to      | et al.  |
| Perc    |         | middle  |         | rations | extreme | 2022;   |
| entiles |         | 50% of  |         | vs.     | values  | Li et   |
| (P25,   |         | cons    |         | rare,   | and     | al.     |
| P50,    |         | umption |         | highly  | defines | 2018;   |
| P75)**  |         | data.   |         | in      | typical | Ihsane  |
|         |         |         |         | tensive | b       | et al.  |
|         |         |         |         | \"un    | aseline | 2018.   |
|         |         |         |         | usual\" | usage.  |         |
|         |         |         |         | demands |         |         |
|         |         |         |         | (out    | **      |         |
|         |         |         |         | liers). | Cons:** |         |
|         |         |         |         |         | Ignores |         |
|         |         |         |         |         | the     |         |
|         |         |         |         |         | chrono  |         |
|         |         |         |         |         | logical |         |
|         |         |         |         |         | seq     |         |
|         |         |         |         |         | uencing |         |
|         |         |         |         |         | of the  |         |
|         |         |         |         |         | loads.  |         |
+---------+---------+---------+---------+---------+---------+---------+
| **      | Com     | Ge      | Es      | C       | **      | Köhler  |
| Fractal | plexity | ometric | timated | aptures | Pros:** | et al.  |
| Di      | M       | com     | via     | str     | Except  | 2022.   |
| mension | easures | plexity | mathe   | uctural | ionally |         |
| (FD) /  |         | ind     | matical | com     | good at |         |
| Length  |         | icating | esti    | plexity | me      |         |
| of      |         | ro      | mators. | of      | asuring |         |
| Curve** |         | ughness |         | beh     | the     |         |
|         |         | or      |         | aviour. | natural |         |
|         |         | vol     |         | R       | ro      |         |
|         |         | atility |         | eflects | ughness |         |
|         |         | of the  |         | the     | of      |         |
|         |         | load    |         | natural | human   |         |
|         |         | traj    |         | sto     | be      |         |
|         |         | ectory. |         | chastic | havior. |         |
|         |         |         |         | sp      |         |         |
|         |         |         |         | ikiness | **      |         |
|         |         |         |         | of      | Cons:** |         |
|         |         |         |         | human   | A       |         |
|         |         |         |         | inte    | bstract |         |
|         |         |         |         | raction | c       |         |
|         |         |         |         | with    | oncept; |         |
|         |         |         |         | appl    | di      |         |
|         |         |         |         | iances. | fficult |         |
|         |         |         |         |         | to      |         |
|         |         |         |         |         | in      |         |
|         |         |         |         |         | terpret |         |
|         |         |         |         |         | in      |         |
|         |         |         |         |         | s       |         |
|         |         |         |         |         | tandard |         |
|         |         |         |         |         | ele     |         |
|         |         |         |         |         | ctrical |         |
|         |         |         |         |         | units.  |         |
+---------+---------+---------+---------+---------+---------+---------+
| **S     | D       | M       | Sum of  | A       | **      | Zhang   |
| equence | istance | easures | point-t | ssesses | Pros:** | et al.  |
| Dissim  | M       | exact   | o-point | how     | Stand   | 2022;   |
| ilarity | easures | shape   | costs   | c       | ardized | Köhler  |
| /       |         | m       | (e.g.   | hronolo | al      | et al.  |
| D       |         | atching | Eucl    | gically | ignment | 2022.   |
| istance |         | or cost | idean). | aligned | of      |         |
| (DTW,   |         | to      |         | or      | s       |         |
| L2,     |         | align   |         | si      | equence |         |
| LCSS)** |         | one     |         | milarly | shapes. |         |
|         |         | s       |         | shaped  |         |         |
|         |         | equence |         | two     | **      |         |
|         |         | to      |         | occu    | Cons:** |         |
|         |         | a       |         | pants\' | C       |         |
|         |         | nother. |         | daily   | omputat |         |
|         |         |         |         | lives   | ionally |         |
|         |         |         |         | are.    | ex      |         |
|         |         |         |         |         | pensive |         |
|         |         |         |         |         | (esp    |         |
|         |         |         |         |         | ecially |         |
|         |         |         |         |         | DTW).   |         |
+---------+---------+---------+---------+---------+---------+---------+
| **RMSE  | Perf    | Ev      | e.g.    | Ev      | **      | Köhler  |
| / MAPE  | ormance | aluates | \$\\tex | aluates | Pros:** | et al.  |
| / NRMSE | / Fit   | the     | t{MAPE} | how     | Stand   | 2022;   |
| / NVF / | M       | ma      | =       | well a  | ardized | Nti et  |
| MAE**   | easures | gnitude | \\fra   | m       | metrics | al.     |
|         |         | of      | c{1}{n} | odelled | for     | 2020;   |
|         |         | de      | \\sum   | load    | eva     | Adeoye  |
|         |         | viation | \\\     | curve   | luating | &       |
|         |         | or      | \frac{y | rep     | model   | Spataru |
|         |         | exact   | -       | licates | ac      | 2019;   |
|         |         | m       | \\      | true    | curacy. | Kewo et |
|         |         | atching | hat{y}} | beh     |         | al.     |
|         |         | error   | {y}\\\$ | avioral | **      | 2023;   |
|         |         | between |         | vari    | Cons:** | Ihsane  |
|         |         | m       |         | ations. | Heavily | et al.  |
|         |         | easured |         |         | pe      | 2018;   |
|         |         | and     |         |         | nalizes | Do      |
|         |         | sy      |         |         | re      | minguez |
|         |         | nthetic |         |         | alistic | et al.  |
|         |         | time    |         |         | raw     | 2021;   |
|         |         | series. |         |         | p       | Widén   |
|         |         |         |         |         | rofiles | et al.  |
|         |         |         |         |         | simply  | 2009.   |
|         |         |         |         |         | for     |         |
|         |         |         |         |         | slight  |         |
|         |         |         |         |         | chrono  |         |
|         |         |         |         |         | logical |         |
|         |         |         |         |         | shifts. |         |
+---------+---------+---------+---------+---------+---------+---------+
| *       | F       | Mean    | \       | Speci   | **      | Ihsane  |
| *MPDADA | orecast | Per     | $MPDADA | fically | Pros:** | et al.  |
| &       | Error   | centage | =       | ev      | More    | 2018    |
| MP      | Metric  | De      | \\f     | aluates | se      |         |
| DADMA** |         | viation | rac{1}{ | how     | nsitive |         |
|         |         | Against | K}\\sum | acc     | to      |         |
|         |         | Daily   | \\      | urately | f       |         |
|         |         | Average | frac{\\ | a model | orecast |         |
|         |         | / Daily | P\_k\^r | p       | errors  |         |
|         |         | Moving  | -       | redicts | during  |         |
|         |         | A       | P\_k\   | the     | c       |         |
|         |         | verage. | ^f\\}{\ | *peak*  | ritical |         |
|         |         |         | \langle | demands | peak    |         |
|         |         |         | P\_i    | c       | times   |         |
|         |         |         | \\ran   | ompared | than    |         |
|         |         |         | gle}\$. | to      | s       |         |
|         |         |         |         | daily   | tandard |         |
|         |         |         |         | av      | MAPE.   |         |
|         |         |         |         | erages. |         |         |
|         |         |         |         |         | **      |         |
|         |         |         |         |         | Cons:** |         |
|         |         |         |         |         | Can be  |         |
|         |         |         |         |         | mathema |         |
|         |         |         |         |         | tically |         |
|         |         |         |         |         | u       |         |
|         |         |         |         |         | nstable |         |
|         |         |         |         |         | if      |         |
|         |         |         |         |         | average |         |
|         |         |         |         |         | daily   |         |
|         |         |         |         |         | load is |         |
|         |         |         |         |         | ex      |         |
|         |         |         |         |         | tremely |         |
|         |         |         |         |         | low.    |         |
+---------+---------+---------+---------+---------+---------+---------+
| B       | Reli    | Shows   | Count   |         |         |         |
| lackout | ability | how     | of gaps |         |         |         |
| Fr      |         | often   | \>      |         |         |         |
| equency |         | the     | (Time   |         |         |         |
|         |         | ho      | Step +  |         |         |         |
|         |         | usehold | Buffer) |         |         |         |
|         |         | exceeds |         |         |         |         |
|         |         | the     |         |         |         |         |
|         |         | 89Wh    |         |         |         |         |
|         |         | battery |         |         |         |         |
|         |         | limit.  |         |         |         |         |
+---------+---------+---------+---------+---------+---------+---------+
| Mean    | Reli    | M       | Average |         |         |         |
| D       | ability | easures | time    |         |         |         |
| uration |         | the     | elapsed |         |         |         |
| of      |         | \"r     | between |         |         |         |
| Outage  |         | ecovery | last    |         |         |         |
| (Dout​) |         | time\"  | r       |         |         |         |
|         |         | (       | ecorded |         |         |         |
|         |         | usually | log and |         |         |         |
|         |         | until   | next    |         |         |         |
|         |         | the     | log.    |         |         |         |
|         |         | next    |         |         |         |         |
|         |         | sunrise |         |         |         |         |
|         |         | p       |         |         |         |         |
|         |         | rovides |         |         |         |         |
|         |         | solar   |         |         |         |         |
|         |         | power). |         |         |         |         |
+---------+---------+---------+---------+---------+---------+---------+
| C       | Timing  | Ide     | The     |         |         |         |
| ritical |         | ntifies | most    |         |         |         |
| Di      |         | if the  | f       |         |         |         |
| scharge |         | b       | requent |         |         |         |
| Window  |         | lackout | hour of |         |         |         |
|         |         | is      | the     |         |         |         |
|         |         | caused  | last    |         |         |         |
|         |         | by      | log     |         |         |         |
|         |         | lat     | before  |         |         |         |
|         |         | e-night | a gap.  |         |         |         |
|         |         | l       |         |         |         |         |
|         |         | ighting |         |         |         |         |
|         |         | or      |         |         |         |         |
|         |         | early-  |         |         |         |         |
|         |         | evening |         |         |         |         |
|         |         | hig     |         |         |         |         |
|         |         | h-power |         |         |         |         |
|         |         | use.    |         |         |         |         |
+---------+---------+---------+---------+---------+---------+---------+
| Reli    | System  | Qua     | T       |         |         |         |
| ability |         | ntifies | otal Th |         |         |         |
| Index   |         | the     | eoretic |         |         |         |
| (RI)    |         | per     | al Hour |         |         |         |
|         |         | centage | sActual |         |         |         |
|         |         | of time |  Record |         |         |         |
|         |         | the     | ed Hour |         |         |         |
|         |         | user    | s​×100. |         |         |         |
|         |         | a       | M       |         |         |         |
|         |         | ctually | easures |         |         |         |
|         |         | has     | the gap |         |         |         |
|         |         | energy  | between |         |         |         |
|         |         | access. | \"De    |         |         |         |
|         |         |         | sired\" |         |         |         |
|         |         |         | and     |         |         |         |
|         |         |         | \"A     |         |         |         |
|         |         |         | ctual\" |         |         |         |
|         |         |         | consu   |         |         |         |
|         |         |         | mption. |         |         |         |
+---------+---------+---------+---------+---------+---------+---------+
| Energy  | System  | E       | Corr    |         |         |         |
| Suff    |         | xplains | elation |         |         |         |
| iciency |         | if      | between |         |         |         |
| Gap     |         | \"aggre | Peak    |         |         |         |
|         |         | ssive\" | Load    |         |         |         |
|         |         | pr      | (LP​)   |         |         |         |
|         |         | actices | and     |         |         |         |
|         |         | lead to | sub     |         |         |         |
|         |         | longer  | sequent |         |         |         |
|         |         | periods | B       |         |         |         |
|         |         | without | lackout |         |         |         |
|         |         | light   | du      |         |         |         |
|         |         |         | ration. |         |         |         |
+---------+---------+---------+---------+---------+---------+---------+
| C       | Con     | Int     | System  |         |         |         |
| limatic | textual | roduces | failure |         |         |         |
| B       |         | \"      | caused  |         |         |         |
| lackout |         | Weather | by low  |         |         |         |
| Rate    |         | S       | v\_pv   |         |         |         |
|         |         | tochast | due to  |         |         |         |
|         |         | icity\" | cloud   |         |         |         |
|         |         | into    | s/rain. |         |         |         |
|         |         | the     |         |         |         |         |
|         |         | demand  |         |         |         |         |
|         |         | model.  |         |         |         |         |
+---------+---------+---------+---------+---------+---------+---------+
| Beh     | P       | Va      | System  |         |         |         |
| avioral | ractice | lidates | failure |         |         |         |
| B       |         | \       | caused  |         |         |         |
| lackout |         | "Aspira | by high |         |         |         |
| Rate    |         | tions\" | usage   |         |         |         |
|         |         | vs.     | (e.g.,  |         |         |         |
|         |         | \"Mat   | c       |         |         |         |
|         |         | erial\" | harging |         |         |         |
|         |         | const   | for     |         |         |         |
|         |         | raints. | neig    |         |         |         |
|         |         |         | hbors). |         |         |         |
+---------+---------+---------+---------+---------+---------+---------+
