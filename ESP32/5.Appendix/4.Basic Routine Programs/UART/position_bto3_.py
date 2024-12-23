action_groups_bto3 = [
      [#1[置中]
          {'id': 1, 'position': 300, 'time': 1000},
          {'id': 2, 'position': 500, 'time': 1000},
          {'id': 3, 'position': 300, 'time': 1000},
          {'id': 4, 'position': 900, 'time': 1000},
          {'id': 5, 'position': 700, 'time': 1000},
          {'id': 6, 'position': 500, 'time': 1000}
      ],
      [#2[b上張1]
          {'id': 1, 'position': 300, 'time': 1000},
          {'id': 2, 'position': 500, 'time': 1000},
          {'id': 3, 'position': 150, 'time': 1000},
          {'id': 4, 'position': 800, 'time': 1000},
          {'id': 5, 'position': 500, 'time': 1000},
          {'id': 6, 'position': 180, 'time': 1000}
      ],
      [#3[b上張2]
          {'id': 1, 'position': 200, 'time': 400},
          {'id': 2, 'position': 500, 'time': 400},
          {'id': 3, 'position': 150, 'time': 400},
          {'id': 4, 'position': 800, 'time': 400},
          {'id': 5, 'position': 450, 'time': 400},
          {'id': 6, 'position': 180, 'time': 400}
      ],
      [#4[b上張3]
          {'id': 1, 'position': 200, 'time': 1000},
          {'id': 2, 'position': 570, 'time': 1000},
          {'id': 3, 'position': 145, 'time': 1000},
          {'id': 4, 'position': 800, 'time': 1000},
          {'id': 5, 'position': 450, 'time': 1000},
          {'id': 6, 'position': 180, 'time': 1000}
      ],
      [#5[b上抓1]
          {'id': 1, 'position': 600, 'time': 1000},
          {'id': 2, 'position': 570, 'time': 1000},
          {'id': 3, 'position': 145, 'time': 1000},
          {'id': 4, 'position': 800, 'time': 1000},
          {'id': 5, 'position': 450, 'time': 1000},
          {'id': 6, 'position': 180, 'time': 1000}
      ],
      [#6[b上抓2]
          {'id': 1, 'position': 600, 'time': 500},
          {'id': 2, 'position': 570, 'time': 500},
          {'id': 3, 'position': 145, 'time': 500},
          {'id': 4, 'position': 800, 'time': 500},
          {'id': 5, 'position': 465, 'time': 500},
          {'id': 6, 'position': 180, 'time': 500}
      ],
      [#7[路上抓]
          {'id': 1, 'position': 600, 'time': 700},
          {'id': 2, 'position': 500, 'time': 700},
          {'id': 3, 'position': 150, 'time': 700},
          {'id': 4, 'position': 800, 'time': 700},
          {'id': 5, 'position': 500, 'time': 700},
          {'id': 6, 'position': 360, 'time': 700}
      ],
      [#8[3上抓1]
          {'id': 1, 'position': 600, 'time': 700},
          {'id': 2, 'position': 500, 'time': 700},
          {'id': 3, 'position': 180, 'time': 700},
          {'id': 4, 'position': 550, 'time': 700},
          {'id': 5, 'position': 300, 'time': 700},
          {'id': 6, 'position': 360, 'time': 700}
      ],
      [#9[3上抓2]
          {'id': 1, 'position': 600, 'time': 500},
          {'id': 2, 'position': 500, 'time': 500},
          {'id': 3, 'position': 180, 'time': 500},
          {'id': 4, 'position': 550, 'time': 500},
          {'id': 5, 'position': 280, 'time': 500},
          {'id': 6, 'position': 360, 'time': 500}
      ],
      [#10[3上放]
          {'id': 1, 'position': 300, 'time': 1000},
          {'id': 2, 'position': 500, 'time': 1000},
          {'id': 3, 'position': 180, 'time': 1000},
          {'id': 4, 'position': 550, 'time': 1000},
          {'id': 5, 'position': 270, 'time': 1000},
          {'id': 6, 'position': 360, 'time': 1000}
      ],
      [#11[置中]
          {'id': 1, 'position': 300, 'time': 1000},
          {'id': 2, 'position': 500, 'time': 1000},
          {'id': 3, 'position': 300, 'time': 1000},
          {'id': 4, 'position': 900, 'time': 1000},
          {'id': 5, 'position': 700, 'time': 1000},
          {'id': 6, 'position': 500, 'time': 1000}
      ]
  ]
# 反轉動作組順序，從1點移動回a點
action_groups_3tob = list(reversed(action_groups_bto3))


