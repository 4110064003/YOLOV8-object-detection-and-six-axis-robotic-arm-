action_groups_b2a = [
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
          {'id': 1, 'position': 600, 'time': 1500},
          {'id': 2, 'position': 570, 'time': 1500},
          {'id': 3, 'position': 145, 'time': 1500},
          {'id': 4, 'position': 800, 'time': 1500},
          {'id': 5, 'position': 500, 'time': 1500},
          {'id': 6, 'position': 180, 'time': 1500}
      ],
      [#7[a上抓1]
          {'id': 1, 'position': 600, 'time': 1500},
          {'id': 2, 'position': 430, 'time': 1500},
          {'id': 3, 'position': 145, 'time': 1500},
          {'id': 4, 'position': 800, 'time': 1500},
          {'id': 5, 'position': 500, 'time': 1500},
          {'id': 6, 'position': 800, 'time': 1500}
      ],
      [#8[a上抓2]
          {'id': 1, 'position': 600, 'time': 1000},
          {'id': 2, 'position': 430, 'time': 1000},
          {'id': 3, 'position': 145, 'time': 1000},
          {'id': 4, 'position': 800, 'time': 1000},
          {'id': 5, 'position': 455, 'time': 1000},
          {'id': 6, 'position': 800, 'time': 1000}
      ],
      [#9[a上放]
          {'id': 1, 'position': 300, 'time': 1000},
          {'id': 2, 'position': 430, 'time': 1000},
          {'id': 3, 'position': 145, 'time': 1000},
          {'id': 4, 'position': 800, 'time': 1000},
          {'id': 5, 'position': 450, 'time': 1000},
          {'id': 6, 'position': 800, 'time': 1000}
      ],
      [#10[置中]
          {'id': 1, 'position': 300, 'time': 1000},
          {'id': 2, 'position': 500, 'time': 1000},
          {'id': 3, 'position': 300, 'time': 1000},
          {'id': 4, 'position': 900, 'time': 1000},
          {'id': 5, 'position': 700, 'time': 1000},
          {'id': 6, 'position': 500, 'time': 1000}
      ] 
  ]
# 反轉動作組順序，從1點移動回a點
action_groups_a2b = list(reversed(action_groups_b2a))







