from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot, ImageSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008774",
        title="물병의 물을 모아 3 L가 되게 하기",
        canvas=Canvas(width=960, height=486, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.q1.copy2",
                    "slot.inserted.image.1",
                    "slot.inserted.image.2",
                    "slot.inserted.image.3",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.label.ga",
                    "slot.label.na",
                    "slot.label.da",
                    "slot.label.ga.copy3",
                    "slot.label.ga.copy3.copy6",
                    "slot.label.ga.copy3.copy6.copy7",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="다음과 같이 물병에 물이 가득 채워져 있습니다. 두 물병의 물을 모아",
                style_role="question",
                x=18.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="",
                style_role="question",
                x=18.0,
                y=58.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.ga",
                prompt="",
                text="㉮",
                style_role="label",
                x=80,
                y=150,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.label.na",
                prompt="",
                text="㉯",
                style_role="label",
                x=330,
                y=150,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.label.da",
                prompt="",
                text="㉰",
                style_role="label",
                x=575,
                y=150,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q1.copy2",
                prompt="",
                text="3 L가 되게 하려면 어느 물병을 골라야 하는지 모두 선택하세요.",
                x=20,
                y=71,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.label.ga.copy3",
                prompt="",
                text="1L 700mL",
                x=100,
                y=350,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.label.ga.copy3.copy6",
                prompt="",
                text="1L 100mL",
                x=330,
                y=350,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.label.ga.copy3.copy6.copy7",
                prompt="",
                text="1L 300mL",
                x=565,
                y=350,
                font_size=28,
                fill="#111111",
            ),
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=111,
                y=151,
                width=118,
                height=144,
                preserve_aspect_ratio="xMidYMid meet",
            ),
            ImageSlot(
                id="slot.inserted.image.2",
                prompt="",
                href="data:image/png;base64,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",
                x=345,
                y=175,
                width=95,
                height=109,
                preserve_aspect_ratio="xMidYMid meet",
            ),
            ImageSlot(
                id="slot.inserted.image.3",
                prompt="",
                href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE4AAAB2CAYAAABmg6XdAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAABzISURBVHhe7Zx3VJTX2rffv771vV9Z3x8xb2JPNclJzoknJzk5J+0k9lhBpPfeEQFFAUtEsWHsmlhiwd5bFFFRaTY6CAoz9N77zADD9a39IEbGzoyI7/G31r14mNnPzN7X3Hvfuz7/wSv1SP+h+cIrPZ1egeuhXoHroV6B66FegeuhehVcR0cHhYWFJMTHcz4igt1hYWxYt55lS5YQFBiEv+9MfGfMwNtzumTieqafH/OCglgaEsL6tesI27mLiHPniL95k4KCAtRqtebX9IqeK7iGhgauxsWxbcsWZs/yx8HWHlNTU6bqGWBlaY2Lsxuent74+s7C3z+AgIAgAgPnETR3gWTiOiBgrvSeSCPSuri4SfdO1ZuKqaGp9Jn+M/3ZunkLcbGx1NXVaWbjuUjn4FQqFRfOn2f+3HlYmZtjoG+Aq6s7s2cHEBwcwpKlKwhZukL623W9OGQ5i0OWsWjxUsmC71rX/+I9kUbzPvE3eNESZs8OxM3Vg2kGhliYWxA0J4hz4eEoFArN7OlMOgPX3t7O/r17sbW2wcjQGD8/f6nQXQVdFLKMhcEh/LRwsU5NfKb47C6Q4nqmnz8mRiZYWlqye1cYra2tmtnVWjoBl5ebi5uTC2am5sxfsJAlS0MlL3keoJ5k4jvFd4s8LFiwCAtzS5wcHMjOytLMtlbSGlxFRQWmxib4+sxkybJQqepoFuZFmciLyNPMmf4YGhpSUlKimf0eS2tw69asxd3NU/qFNTPeV0xUYRFYQpev0Mx+j6U1OCd7RwKD5vcpT9M0kbe5c3/C0c5BM/s9ltbg7Kytpe7B0mWhL6RNe5KJPIm82drYYW5urpn9Hkt7cA5OfPj+MGysbTu7DUuW9wmAUpBYspzFS5ZhZ2vPn94fxo+GFqg6NEvQM2kNztbBiXeGDOWdIUMYPXI006f73OuGPK8uyKNM6prc/W7xI3rP8GXs6LGd+Rs8mAmGlij7CjhXR0fee+ttKXNDBgzgg3ff44fvvsfGxk7q8YuCdPWxRGFEe6MLmOIzxGeJzxSfL2xRyFL8Zwdia+vAiH/9IOVlSP8BUt5EHs0srDWz32NpDc7T3V3K1LtD35Ls7cFDpMwOHTiITz78E99+/Q0GU6fh5OQiDZvEUErqsC5Z3mkPGUmELLlrmq9L74n7Or157ryf8PWbhbOzqzRq+O6bb/nzRx9L3y3yIPLSlS+RR2dXd83s91hagzt54iTvDR3Ku0OG3stkl701aLBUgCEDBkqF+ej9Yfxt+F/5+p9fMWbU6M7xpokZNtZ2ODk6S0MzNzdP3N29JBPX4jUnRxcpjamJOVP1DRgzaoz0GZ8P/4yPhn3QCWrAQOm7xHcKD+uWF6mqDsHTzZ3LFy9SVFioWYxnltbg2tvacZzux7uDBvF2//4PwOsyURjhAaKQg/sPkGyoKOx9Jt4TBRfphIlr8dr96cT1vfsHDpTSPQDq/h+vf3+G9u/P5//4BktjI2zNTHGwsebgvr0olUrN4jy1tAYnFJHXxCC3VXwy/G8M6fcab735hhQsNAvxRJOCTHd7mCc/ycR9Q998g8H9XuPjv/yV7wPXo+82C2sjA6zuwrO3MGfJwp+oqanRLM5TSSfgsmpaeX9fCVbncxk7azmf/vN76Zce8vprDPmv13l74KC7AJ4dwhPtLuC3Bg5i0H+9zqB+rzG0/5t89s/v0JsZgvdFObY3mpls74mtkQG2pibYCXDmZjhZWbAgIICGhnrNIj1ROgHXpGrn7/vkWKWATzZ4xlVgue0s49zm8MWIH/lg2EcSwMGvdxZs8Ov9GPLmG7w1YABv322TunnYXdP0PpFWRO5Bb7xB/3796P/aawzo14+B/V7nw2Ef8O3IcRh5+DNz1xmWJlSwPA/mycAkPJ9JFg7YmxpJwBwszHGyssTJ0hwXGyvWhIZKk6zPIp2AExp/VI5+bDPTUxT4prcRKIMFcpiX0ojf2VRct57ENHAF4yyc+GbsZL74+l988ufhvPfWOwx5800GCaivv87Ah9iAfq9LsERkHP6X4Xz37feMnzAZc1snZgavYOWeU2y7ks5BWTMHy2BHCayVd7DoloLAW61MOHIbPXNbHMyMcbQ0x9nKEldba1ysLXG2Ftc2XLpwQbNIj5XOwM24WMToyHoJ3IzkFmalthCYpuCnzFaW5cDqAthYAFsKYbNMxYbkclZFZ7HibDxLj8ew5OB5gneeIPi3Iyzcsp9FW/ezfOcR1uw9yZbjF9gTEcux6CQupchJKqhG3tBBthJSW+B6E0RWw7GiDsJyWvk1W8mq28p74L7bncpUM2vszUwkWG621rjb20rmZmeDh70t/t5e1Nc/fZXVGbhfkir5++mqB8AtSFewOEPB8kwFq28r2ZCtYrO8jZ0FsLcYjpTDyUoIr4ELtXClHmIbOmEkNEOaAjJVkN0K8lbIU0KBEnKaIK1WzfXKdi6XtXG2qI0j+a2E5ai6gQvIVPPl5msYmVriaGGKq40V7nY2eDrY4eVgJ/0VNt3JgTMnT2gW65HSGbhweT0fHi5jeqry8eCylFLBfpOr2JmjYm+uioN5rRwraOVUYSvhxW1cKGmTYMSUt0tgEqraSalpJ71WzZ06NfIGNbJ6Nak1ne8/EtztVgLSFFgFb8TUzBInCzPJ24SHeTva4+3kIAGb7mjPDGdH5vjMoKmxUbNoD5XOwMWXNPHVpmimZ6iZkaJ44eBWZ7dL4AJ/3Yuv13QsrGylYCC8zesuKB9XZ3xcnCSbIczZkZjLlzWL9lDpDNzt6lbMA1fifSSGGZkwK6P9hYDbndvGlgJYmVZP4PodzHF3xs/HFxsbW5ytzCVvE14mIPm6OneamzO+7s7MdHclNGQR6qeIsDoDl9+oxiFoKd6Odnit34NfXAlBd+CnbAi508by28rnBu5KeTsR5XCiHAncynPxzJ4XjJ+zHQFe7vj5+EngXKwsuoNzc8bPzQU/dxcJ2iwPN2a4ujzVkExn4Aqb1DjNX4G3vTXu5sa4uXngvWobc35PZGFCJaGyDtblwi8FsLUAdhRAWL6affltHMxv41hBG6cK2x4BTk1KjZpbdR1kN0K+ojNA3FZAUiNEi4iaUcHGU1HMXbQcbyd7ZjjaMtPDjYDpHvfAuVpbdrZvTg5SNRXQBDCRTkCTzNOdyIgIzeI9IN2Dc7ST2hFXC1OcTKZJfScXdy+8Fixj9q/7CT4ezcrLmWyIL2JbRq3kcUdL4HQ5hFfCxWqIqoG4OrhR3wkmrQkyW+B2I2RUqUgpquFqRh4noxPYvO8oC5eE4uPlhZuoitYWzHB2wFdA0QRnY4mHg50ETbwv2jYpnQTPFX8PN/y9PFi/aqVm8R7Q8wNnYyV1Lh0tzLAzmoaNgR6WUydjrj8ZCyNDab7O3sUd5+l+uM8MxDsoGL+Fy5gd8jNBK9ax4OcNLBS2Yg0Ll/3M/OAQaWV/1kx/vD08cLa2xtZ4GnbG03AwMcLVygLPrmrYBeQh4LydHZnu7MC8ObPxcnTE08G+0/tEdfVwZbaXB/Nmz6KpqUmziN30/MFZmkvDHDE+tDE1xsrIEHODqZjoTcZw4ngMxo1Bb8woJo0ayYSRPzB+xPdMGDmCSaNHMmXMaPTGjWHq+HFSWuNJEzDTn4KV4VRsTYylH0V0aF1trHG3s73XH3sUOE97GzauXk1RUaG0gF5RXs6WjRtxs7WR2jvhef6e7vi5OpObk6NZxG7qfXDGRlgYTsNsmgEmU/Ux1puC4ZTJGEyahP7ECehNGI/+xIkYTJ6E4ZQpGOvrYWowVbpHQLcxMcbOzKRzkC7Gmk8JzszUguXBP0nTYJpavnihFF2F14l2Ttx3JzNTM1k3/VuA853hi4ODE/JHrOYnJSTgbm/XzeuSExI0k3XTvwU4by9vQpaGamb5nsRuBG9Xl3ttnWjnDoTt0kzWTf8W4Lw8vDh19rxmlu9J7LBaGDRHirKiiyLAbd20QTNZN/17gPOczi15vmaWu0mMGKRuiqsz/l7ubFj1aA8V+m8PLtDLnRlzFpBd9fjuhQAljV9dnJjt6c760F4E5zJvWd8C5+4igZuw8jiFjY/f8vrr+nXSfQKcCA7rf+5FcIYLN+Nta9k3wLk4MtPZnllbj/DerjxSy1s0s9xNm9atvXuvI7M83Xqxqja0MXx7Ku5zF+NuboSrmKJ+EeAc7ZluZ42vqxNBO44zJ13FwB05TD4sp6Xt0V63fvXPeDjYSiMLMYLYsLKXwOXWKPhkTw6u12vxWrMdVwd7nIwNcBDDorsrS88TnKu1FW6WZnjaWjJn3kJCwhNYnKUmIKON4WHZDN6Yzo3SR3vd2tBQaRwrvE705datXK6ZpJt0Bu52lYIPwmR4pqvxuaXGN1KG94bduPnMwt7C7I+xqt4kzPQmY6IvoEzBeMpkDCdPwmDiRPQnjEdv/I/oT5iAwaSJGE6eLIE1naqPxTQDrAynYW1shI2xIdYCoqFB51jV1AhPJyfmLVrOqpNX+CWzkTU5sChDydwMFR/tljF04y0yqx+9mXrZ4uDO6XRHe6kvt6G32riE0mbe3iW/O3WuwD9TTVAWzE9uYN6FW8wJ+x2fZetwmxmAg7MblubmEjSDH8eiN240k0ePYuKoEdJ4deKokUwaM4opY8eg/+NYDCb8iNGkiZhMnoi5vh4OluZ4u7kTFBBE6NpN/HbyAgcS8zla2C6tY4g1jTV3VITeUTEzuYV+W2X4XSrmUdOTYtwaHBQkeZwEzs2ZtaGP372pM3AXcuv54GDxg4s1Ga0skUFoDqzNhY2yVtYnV7Luag6rL6ay+uwNVv9+lbWnoll74jLrj19i04lLbD4ZyW+nr7DrTBT7ImI4HHmNE1HxnLuWSmy6nKT8SlKr20hsgNg6OF8Bxwrbpbm9XXmthGYqmHa+nCHbs/mf69JJekxwaGxoZI6vLx72YuGmc7ZkzYplmsm6SWfgtqdW89mJigfBaUydb8xuZUuump2FsKcEDpXBsXL4vRLOVUFkDUTVQlw93GyA5CZIb+6ctBTLgXkqKFRBXguk13WQUtvBzeoOrpSrOZrfyqLEevTPlPDe9iw+2CXD/Eo17+zOx/B4Lsr2h/tcWWkZHs5O9wKMALdx9SrNZN2kM3ALYkr57lzNE8HpaupcXq8mqaqN3VlNzLtezdTTRQzfI+NPu7IZeawAz7gaQjKVLMxsldq4/wxNJrHi4W1cdtYdKfqL6SXhdT6uTuzYslkzWTfpDJzd2XzGX2nsNXA5DWriylqZeDyffx3KxeFCGQsT6tiarZCqqvDsxbcUzLul4i8HC/i/q5PJrFFpZlvSlUuRON3XrRFdkiMH9msm6yadgRtzWIZBXEuvgROLNSnVne9fr1JLVfX34nb25nau5K+5o2TFHRWzUxUMCcvHMTwf9cNrKju2bcXZxkraR9IF7kpkpGaybtIJuJZWNf/YK8f8hgKv5N4DJ1a5bla1c+Xu8qBo4w7kt0oeJxakLS5V8vaObP7XL9n8nvPw7Q3i9GHw3Lm42Apw1rjZ2UrRNfNWumbSbtIJuIJ6FZ+EybBLVOKZ3NKr4JJq1Nyo7vS4k0VtrEhrxCSiTAoM7+7IxuBiJZ8eKcHwRC6qhwSH8rIyaRJTVFUBTkCb4e5GWWmpZtJu0gm4xNJmhm6X4ZqiwiOp98AlV7dzSN7MkoQaLM+V8Pk+OR/vzOarQ3k4RlUTfEtB8O1WvjtVyv8ITST5IcEhLiYGR2tLaduXqKoiqi6cN5e2tjbNpN2kE3BnZPV8eKgU12RFr4G7FxxO5POP/XLMzhYTcK2Gjbdb2JnbKvUXQzJEcFAyJryC/7M6ifSqB8GJMarwNkcri3vgdm7bopnsAekE3PqECr44XdWr4Lo8LqqslauVnVX1THE7+/I6g8Pqu8EhME3JxweLmXhEjmZNra6qwsPBXhqJOFmKvXJW0qachBs3uid8iHQCzjeymB8u1PU6ONHGxYuIel9wEOBEcFiXpcIuupr3dsn5f1vkzI568ORgxNkz0l5gu7u7NIXH+bi5UVf75FPWOgE39UQOE6KbcHkB4BKr1fe6I6eL21mb0YxNZDkf75bz1m9ZTDpXzvdnqxh3WM79s0pKlRJ/Hx9pAkLMtAhwYpfm1k0b7y/aI6U1OOH93x6UM/VqCy5JvQtO9ONO5SlYnVKHS2QZXx3IlYLD3/blYHmpggVpLVJwMI6q5T9XppJa+Ucbd+niRWzNzDp3oN8F52hp8cT11C5pDa5W0c5ne+WY3FDgnNTSa+BEcIgtU0kjh8/3yJhyqoAZMVWsSm9ie04rm6TgoGTuLSWWsfX877Vp98CJLavebm4SNGGiqor2bWnwgqfeRK01OFm1kmE7s7BKVOKU2HvguoJDRJGK6HKx1UvN2ZJ29ue1slkEh9tKlt9WSeC+PFnOF7uy7gWHrb/8IsGyNjH+Y/u+hTnpqamaxXuktAYn+nCDf8vGLrn3wYk2LkHq/P6xsXBvXqvUHVmfrcI1rpaP9uTw5o5cvjvYuRfkYsQ5aSZaQBNmY2oiVdFN69dpFu2x0hrcpbxG3t5fhF2S4oWBu3Y3OIjuyOY7ClyjKvlsbw6Dt91h1OkS7G+28M9D+ZwMPy/NHFubGElT+MKEt/m4u1NVValZtMdKa3CHb9fy0bHyFwbufJGKX2414BNdyYgjeXy8K5u/7JZjGFFGYHIzP2WqcE5S8kXIYWmXlIBlaWQomfA24X1pKSmaxXqitAa3KamS4acqex1c58hBxaQTncFh1NE8XC6XsyS5gW1ylRQclmQqpV3nrskqvg7ejeXUKdKij9ifJ6qpgBh16ZJmkZ5KWoMLji3ly/CaXgcnPE5MZJ7MU3CxpJXLZZ3BQcyOiODQdc5hTqoCz7RWvlx2FHP9TnDC0+wtTIl+yh3mD5PW4GZeKuLbC3UvBFza3Q5w1H3BQfOAiADnldbGl6vCsTTQw9bcDB9vz2eKoA+T1uCczhUw4nLDCwH3sO36jwL39cbL0ph01/bfqNfBg6u0Bmd8OpfRUY19Gpx3qpJP9+dw+NrTjQqeRlqDG3s0h3ExTdgl9l1wM1IVfHKikhOyZs3s91hag/vhsJwJcc19Htxnpyr4LaVKM/s9ltbgvj6Qw6SrLdgmtvRpcF+eqWJNfIVm9nssrcC1tqml2dcp1/o+uG/O1bA4rkyzCD2WVuAaFW3SPL/+9b4P7vsLdQRceXAys6fSClx1UyvDd8swuKHANqFvgxsZWS+d4taVtAJXWq/i4zA5hvEKbPo4uLGXG3CJePKpwKeVVuDya5V8uEeO8UsAbnxUI9ZnCjSL0GNpBU5WpWBYmByThL4PbmJ0E4Yn8zSL0GNpBe52hYL3dmRhlqjs2+BSFEyKbWbi8VzNIvRYWoFLL2vm7Z0yzJP6NjjvFAVT4loYfeTxJwKfRVqBSy5pYsj2Oy8FOP2rLdIoR1fSCtzNokYG78jGPKlvt3ECnMG1Fr45KHvqVawnSStwVwsaGCTAJfZ9cIbXFXy1PxtVWx8AF5PfyOCwvJcCnPENBV8ekNGkevQhkWeRVuCi8hoYsjsf88SWPg6uBZObCj7fL6dO8eAJ6Z5IK3BX8hoYuq+wz4ObntyC2U0Ff90np6r58fvenlZagYvMqWfo/uKXApx5vJJPd2dT1qibJ+1rBe5iTj3vHCx5KcBZJCj58x4ZRfUP33n+rNIK3JnsupcGnNjb8uFuGXm1PX+g6P3SGty7h0pfCnDWiUqG7cpC9piDcM8ircAdv13D+4dfDnA2SUreD5Nxu+rRZ7qeRVqBO5pZw7CXAJxXcgt2ySre2SUjvaIPgDt4q5oPjpa/NOCG7swipawPgNvXQ3BbZCp25bayN7+NwwVtHC9s53RxG2cFtNJ2LpW1E13RzrVKtbTFQTwL805DB3LxCLQmKGruIK+xQ9oC8fTglAzeKSOh5PFPg3ha9Qo4sWvo5ywl67NUbMxSsjqjmeUpjSxOqGf+9Rpmx1bhH1OJf3QlsyWrICCmgrmxFSy8WsmS61WExlfza2odh+40cj6/hetlKskLxcmaq1Vqzpe0S7vOHwduyC458SW6WZR+buD801qYf0vJwltKApMa8Y6rwfFiObbnS7E7X4prZDneURUEXq1mSUIdq1Ma2JTeyG+ZTey608yerGb2ZzdzILuZfXcaCctsYHNqHaviq1l6vZL5MeUERJUzP7aS1Ul10j2dZ7naJI9+AFyS8Lgsrhf3EY/70/GKB8D5pSrwS27GKaoGk/BSTM+W4BBZwezrdSxNbWJTlpIdOaKqtt6rquLkX3hJGxfLOh/dGHv3VKDwKHGgt6uq5jVBQXMH2fVqLhcr2XOnkcU3qvGKLMP1QikBV6tZm9kibWUVxy67gduRzdWip3vq6pOkc3BeKQpsomrQO12MeUQ5PjfqWZSh4OcslVSYX8RzgHUQHMRB34w6Nck1HVJVFff9mtGMb3QllmeL8Yyukr5XbCzsBKdg8O48Ygr7KLhp58qZeqYEr5uNUlUNzlBKZ6qed1QNL2rjRGEbBwraWJPZgsPFckzDS/FPaZH6cQLc0L0FROX3AXBhaX+As01UYBhZxdTwUnxTFcxOUzwyqj4PcPdH1S1yFeuyVThdqcQ0okyaj7MXVTUsl9i+4HFhaVV8dKISi8QWrOObmXCqGLfEZnz6wAOURXBYnKnE8EwJLjcbsU1S8s7OLO70hSHX5dx6Bu/NxyJJgdXNJiaeLsY9qQWfJ/Tjeguc6AYZnS3B9WYj+lfF1LmMVs0jhD2UVuDqWtr4ZGcmU64rcEhWMDWiAqPzFfilKaTuyIsCt1mmZJ1MhWdsDcbhpfilqfjgSDlbkp7tLMPjpBU4oa3JVQzeV4xtkko6BKd3pgSjc2X4JjUzP0Ml9eN6C5x4CLPox/2SrcQjqgqj34sJSlMw9lITYw/LdeZtQlqDE/I8X8C7h8oleL7pSiwiK6XuiO3lKmYnNrH0thg5qKQzpBuzdQcurbZz17nojoih2m6ZgnnXa7EOL8H9ciWLM1WMv9zC38NkFDXoZgKzSzoBJ9Yqg2NK6L81i0kxCmZltOGf0ozd5SqMzpRgca4Uz5hqFiQ2SF0FEfXEYVzxuG7RAT5W2MapojbOFLdxXoxVSzvHquLkszhylFqjJrNejawRCpqguEU8W72DRHHOIbeF9Sn1zIyqwOVCKf6xVVIHeH6Gms+OlqF/PI9SHUMT0gm4LsXmNzDxWC5Dd8jQi1UyK0PN4sxWghIb8Yqpxv5CGbYRpThdLGP6lUqpl780sZ7VqY1szmhi551m9ssVHM1RciJPyak8Jb/nKTiV28LxnGYOZjWxPb2etQnVhFyrJDC6nLkxFYTG10r3HshvZ3kWjDtXw2c7s9icUIH6UQ8b0VI6BdelSzn1OIQXMHy3nOFHSjGNU+B/q4PQ7A42yFpZfauZFSmNBMfXMfdaNQGxVcyJ6Rzg+0dXSIP8OdEVzI2pZGFcJUuvV7EqoZpNybXszWwgIq+FuFIV8dUdXKiErbngerVZOvg24pCcTfEVVDXpZlHmUXou4LpU1qDi1O1afC8WM/KQnL/vkfFpWDbjImqxiWtmVkorizLV/JwNm3Jhez7sLYRDxXCsBE6UwqkyOFkKx0rhYBFsk7cTkqrA/kotIw7k8v2hXCYek7PqegUJRboZwD+Nnis4TZXUqbhe0MiRzFpWXC1j+vlCTE7m8uMROWMP5zL6UA4jD+cwQlwfzpWuxx6RM+5wDhOOyDE+kcuMiEJWXi3jRGYNiYWN1OlonfRZ1avgniTxuB6lqp0WZaeJ6+fVRmmrPgXuZdIrcD3UK3A91CtwPdQrcD3UK3A91P8HsrfFAiL5vuoAAAAASUVORK5CYII=",
                x=592,
                y=165,
                width=78,
                height=118,
                preserve_aspect_ratio="xMidYMid meet",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008774",
    "problem_type": "multiple_choice_selection",
    "metadata": {
        "language": "ko",
        "question": "두 물병의 물을 모아 3 L가 되게 하는 물병을 모두 고르는 문제",
        "instruction": "어느 물병을 골라야 하는지 모두 선택한다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.bottle.ga",
                "type": "bottle",
                "label": "가",
                "capacity": {"l": 1, "ml": 700},
            },
            {
                "id": "obj.bottle.na",
                "type": "bottle",
                "label": "나",
                "capacity": {"l": 1, "ml": 100},
            },
            {
                "id": "obj.bottle.da",
                "type": "bottle",
                "label": "다",
                "capacity": {"l": 1, "ml": 300},
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.bottle.ga", "obj.bottle.na", "obj.bottle.da"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.target_sum"],
            },
            "plan": {
                "method": "pair_selection",
                "description": "주어진 물병들 중 두 개를 골라 합이 3 L가 되는 조합을 찾는다.",
            },
            "execute": {
                "expected_operations": ["compare_capacities", "add_two_bottles", "match_target_sum"]
            },
            "review": {"check_methods": ["target_sum_check", "selection_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_bottles",
            "description": "3 L가 되게 하는 물병의 조합",
            "count": 2,
        },
        "value": "가, 다",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008774",
    "problem_type": "multiple_choice_selection",
    "inputs": {
        "total_ticks": 3,
        "target_label": "3 L",
        "target_ticks": 3,
        "target_count": 2,
        "unit": "L",
    },
    "given": [
        {"ref": "obj.bottle.ga", "value": {"l": 1, "ml": 700}},
        {"ref": "obj.bottle.na", "value": {"l": 1, "ml": 100}},
        {"ref": "obj.bottle.da", "value": {"l": 1, "ml": 300}},
    ],
    "target": {"ref": "answer.target", "type": "selected_bottles"},
    "method": "pair_selection",
    "plan": ["각 물병의 용량을 비교한다.", "두 물병을 더해 3 L가 되는 조합을 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "1 L 700 mL + 1 L 300 mL", "value": {"l": 3, "ml": 0}},
        {"id": "step.2", "expr": "3 L = 3 L", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "가 물병과 다 물병의 합이 3 L인지 확인",
            "expected": {"l": 3, "ml": 0},
            "actual": {"l": 3, "ml": 0},
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_bottles",
            "description": "3 L가 되게 하는 물병의 조합",
            "count": 2,
        },
        "value": "가, 다",
        "unit": "",
    },
}
