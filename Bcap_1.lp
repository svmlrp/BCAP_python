\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  0 B[1,1,1,1] + 0 B[1,1,1,2] + 0 B[1,2,1,1] + 0 B[1,2,1,2] + 0 B[1,3,1,1]
   + 0 B[1,3,1,2] + 0 B[1,4,1,1] + 0 B[1,4,1,2] + 0 B[2,1,1,1]
   + 0 B[2,1,1,2] + 0 B[2,2,1,1] + 0 B[2,2,1,2] + 0 B[2,3,1,1]
   + 0 B[2,3,1,2] + 0 B[2,4,1,1] + 0 B[2,4,1,2] + 0 B[3,1,1,1]
   + 0 B[3,1,1,2] + 0 B[3,2,1,1] + 0 B[3,2,1,2] + 0 B[3,3,1,1]
   + 0 B[3,3,1,2] + 0 B[3,4,1,1] + 0 B[3,4,1,2] + 0 B[4,1,1,1]
   + 0 B[4,1,1,2] + 0 B[4,2,1,1] + 0 B[4,2,1,2] + 0 B[4,3,1,1]
   + 0 B[4,3,1,2] + 0 B[4,4,1,1] + 0 B[4,4,1,2] + 0 B[5,1,1,1]
   + 0 B[5,1,1,2] + 0 B[5,2,1,1] + 0 B[5,2,1,2] + 0 B[5,3,1,1]
   + 0 B[5,3,1,2] + 0 B[5,4,1,1] + 0 B[5,4,1,2] + 0 adjcargo2[1,1,1,1]
   + 0 adjcargo2[1,1,1,2] + 0 adjcargo2[1,2,1,1] + 0 adjcargo2[1,2,1,2]
   + 0 adjcargo2[1,3,1,1] + 0 adjcargo2[1,3,1,2] + 0 adjcargo2[1,4,1,1]
   + 0 adjcargo2[1,4,1,2] + 0 adjcargo2[2,1,1,1] + 0 adjcargo2[2,1,1,2]
   + 0 adjcargo2[2,2,1,1] + 0 adjcargo2[2,2,1,2] + 0 adjcargo2[2,3,1,1]
   + 0 adjcargo2[2,3,1,2] + 0 adjcargo2[2,4,1,1] + 0 adjcargo2[2,4,1,2]
   + 0 adjcargo2[3,1,1,1] + 0 adjcargo2[3,1,1,2] + 0 adjcargo2[3,2,1,1]
   + 0 adjcargo2[3,2,1,2] + 0 adjcargo2[3,3,1,1] + 0 adjcargo2[3,3,1,2]
   + 0 adjcargo2[3,4,1,1] + 0 adjcargo2[3,4,1,2] + 0 adjcargo2[4,1,1,1]
   + 0 adjcargo2[4,1,1,2] + 0 adjcargo2[4,2,1,1] + 0 adjcargo2[4,2,1,2]
   + 0 adjcargo2[4,3,1,1] + 0 adjcargo2[4,3,1,2] + 0 adjcargo2[4,4,1,1]
   + 0 adjcargo2[4,4,1,2] + X[1,1,1,1] + X[1,1,1,2] + X[1,2,1,1]
   + X[1,2,1,2] + X[2,1,1,1] + X[2,1,1,2] + X[2,2,1,1] + X[2,2,1,2]
   + X[3,1,1,1] + X[3,1,1,2] + X[3,2,1,1] + X[3,2,1,2] + X[4,1,1,1]
   + X[4,1,1,2] + X[4,2,1,1] + X[4,2,1,2] + X[5,1,1,1] + X[5,1,1,2]
   + X[5,2,1,1] + X[5,2,1,2] + 0 b_holdasballast[1,1]
   + 0 b_holdasballast[2,1] + 0 b_holdasballast[3,1] + 0 cb_hold[1,1]
   + 0 cb_hold[2,1] + 0 cb_hold[3,1]
Subject To
 lowerboundHold_1: X[1,1,1,1] >= 0
 MaxCapacityHold_1: X[1,1,1,1] <= 20894
 lowerboundHold_1: X[1,1,1,2] >= 0
 MaxCapacityHold_1: X[1,1,1,2] <= 20894
 lowerboundHold_1: X[1,2,1,1] >= 0
 MaxCapacityHold_1: X[1,2,1,1] <= 20894
 lowerboundHold_1: X[1,2,1,2] >= 0
 MaxCapacityHold_1: X[1,2,1,2] <= 20894
 lowerboundHold_1: X[1,3,1,1] >= 0
 MaxCapacityHold_1: X[1,3,1,1] <= 20894
 lowerboundHold_1: X[1,3,1,2] >= 0
 MaxCapacityHold_1: X[1,3,1,2] <= 20894
 lowerboundHold_1: X[1,4,1,1] >= 0
 MaxCapacityHold_1: X[1,4,1,1] <= 20894
 lowerboundHold_1: X[1,4,1,2] >= 0
 MaxCapacityHold_1: X[1,4,1,2] <= 20894
 lowerboundHold_2: X[2,1,1,1] >= 0
 MaxCapacityHold_2: X[2,1,1,1] <= 23912
 lowerboundHold_2: X[2,1,1,2] >= 0
 MaxCapacityHold_2: X[2,1,1,2] <= 23912
 lowerboundHold_2: X[2,2,1,1] >= 0
 MaxCapacityHold_2: X[2,2,1,1] <= 23912
 lowerboundHold_2: X[2,2,1,2] >= 0
 MaxCapacityHold_2: X[2,2,1,2] <= 23912
 lowerboundHold_2: X[2,3,1,1] >= 0
 MaxCapacityHold_2: X[2,3,1,1] <= 23912
 lowerboundHold_2: X[2,3,1,2] >= 0
 MaxCapacityHold_2: X[2,3,1,2] <= 23912
 lowerboundHold_2: X[2,4,1,1] >= 0
 MaxCapacityHold_2: X[2,4,1,1] <= 23912
 lowerboundHold_2: X[2,4,1,2] >= 0
 MaxCapacityHold_2: X[2,4,1,2] <= 23912
 lowerboundHold_3: X[3,1,1,1] >= 0
 MaxCapacityHold_3: X[3,1,1,1] <= 21445
 lowerboundHold_3: X[3,1,1,2] >= 0
 MaxCapacityHold_3: X[3,1,1,2] <= 21445
 lowerboundHold_3: X[3,2,1,1] >= 0
 MaxCapacityHold_3: X[3,2,1,1] <= 21445
 lowerboundHold_3: X[3,2,1,2] >= 0
 MaxCapacityHold_3: X[3,2,1,2] <= 21445
 lowerboundHold_3: X[3,3,1,1] >= 0
 MaxCapacityHold_3: X[3,3,1,1] <= 21445
 lowerboundHold_3: X[3,3,1,2] >= 0
 MaxCapacityHold_3: X[3,3,1,2] <= 21445
 lowerboundHold_3: X[3,4,1,1] >= 0
 MaxCapacityHold_3: X[3,4,1,1] <= 21445
 lowerboundHold_3: X[3,4,1,2] >= 0
 MaxCapacityHold_3: X[3,4,1,2] <= 21445
 lowerboundHold_4: X[4,1,1,1] >= 0
 MaxCapacityHold_4: X[4,1,1,1] <= 23933
 lowerboundHold_4: X[4,1,1,2] >= 0
 MaxCapacityHold_4: X[4,1,1,2] <= 23933
 lowerboundHold_4: X[4,2,1,1] >= 0
 MaxCapacityHold_4: X[4,2,1,1] <= 23933
 lowerboundHold_4: X[4,2,1,2] >= 0
 MaxCapacityHold_4: X[4,2,1,2] <= 23933
 lowerboundHold_4: X[4,3,1,1] >= 0
 MaxCapacityHold_4: X[4,3,1,1] <= 23933
 lowerboundHold_4: X[4,3,1,2] >= 0
 MaxCapacityHold_4: X[4,3,1,2] <= 23933
 lowerboundHold_4: X[4,4,1,1] >= 0
 MaxCapacityHold_4: X[4,4,1,1] <= 23933
 lowerboundHold_4: X[4,4,1,2] >= 0
 MaxCapacityHold_4: X[4,4,1,2] <= 23933
 lowerboundHold_5: X[5,1,1,1] >= 0
 MaxCapacityHold_5: X[5,1,1,1] <= 20816
 lowerboundHold_5: X[5,1,1,2] >= 0
 MaxCapacityHold_5: X[5,1,1,2] <= 20816
 lowerboundHold_5: X[5,2,1,1] >= 0
 MaxCapacityHold_5: X[5,2,1,1] <= 20816
 lowerboundHold_5: X[5,2,1,2] >= 0
 MaxCapacityHold_5: X[5,2,1,2] <= 20816
 lowerboundHold_5: X[5,3,1,1] >= 0
 MaxCapacityHold_5: X[5,3,1,1] <= 20816
 lowerboundHold_5: X[5,3,1,2] >= 0
 MaxCapacityHold_5: X[5,3,1,2] <= 20816
 lowerboundHold_5: X[5,4,1,1] >= 0
 MaxCapacityHold_5: X[5,4,1,1] <= 20816
 lowerboundHold_5: X[5,4,1,2] >= 0
 MaxCapacityHold_5: X[5,4,1,2] <= 20816
 lowerboundBallast_1: tnk_ballast[1,1] >= 0
 upperboundBallast_1: tnk_ballast[1,1] <= 3424.525
 lowerboundBallast_1: tnk_ballast[1,2] >= 0
 upperboundBallast_1: tnk_ballast[1,2] <= 3424.525
 lowerboundBallast_1: tnk_ballast[1,3] >= 0
 upperboundBallast_1: tnk_ballast[1,3] <= 3424.525
 lowerboundBallast_2: tnk_ballast[2,1] >= 0
 upperboundBallast_2: tnk_ballast[2,1] <= 2674.1225
 lowerboundBallast_2: tnk_ballast[2,2] >= 0
 upperboundBallast_2: tnk_ballast[2,2] <= 2674.1225
 lowerboundBallast_2: tnk_ballast[2,3] >= 0
 upperboundBallast_2: tnk_ballast[2,3] <= 2674.1225
 lowerboundBallast_3: tnk_ballast[3,1] >= 0
 upperboundBallast_3: tnk_ballast[3,1] <= 2674.1225
 lowerboundBallast_3: tnk_ballast[3,2] >= 0
 upperboundBallast_3: tnk_ballast[3,2] <= 2674.1225
 lowerboundBallast_3: tnk_ballast[3,3] >= 0
 upperboundBallast_3: tnk_ballast[3,3] <= 2674.1225
 lowerboundBallast_4: tnk_ballast[4,1] >= 0
 upperboundBallast_4: tnk_ballast[4,1] <= 3666.22
 lowerboundBallast_4: tnk_ballast[4,2] >= 0
 upperboundBallast_4: tnk_ballast[4,2] <= 3666.22
 lowerboundBallast_4: tnk_ballast[4,3] >= 0
 upperboundBallast_4: tnk_ballast[4,3] <= 3666.22
 lowerboundBallast_5: tnk_ballast[5,1] >= 0
 upperboundBallast_5: tnk_ballast[5,1] <= 0
 lowerboundBallast_5: tnk_ballast[5,2] >= 0
 upperboundBallast_5: tnk_ballast[5,2] <= 0
 lowerboundBallast_5: tnk_ballast[5,3] >= 0
 upperboundBallast_5: tnk_ballast[5,3] <= 0
 lowerboundBallast_6: tnk_ballast[6,1] >= 0
 upperboundBallast_6: tnk_ballast[6,1] <= 0
 lowerboundBallast_6: tnk_ballast[6,2] >= 0
 upperboundBallast_6: tnk_ballast[6,2] <= 0
 lowerboundBallast_6: tnk_ballast[6,3] >= 0
 upperboundBallast_6: tnk_ballast[6,3] <= 0
 lowerboundBallast_7: tnk_ballast[7,1] >= 0
 upperboundBallast_7: tnk_ballast[7,1] <= 0
 lowerboundBallast_7: tnk_ballast[7,2] >= 0
 upperboundBallast_7: tnk_ballast[7,2] <= 0
 lowerboundBallast_7: tnk_ballast[7,3] >= 0
 upperboundBallast_7: tnk_ballast[7,3] <= 0
 lowerboundBallast_8: tnk_ballast[8,1] >= 0
 upperboundBallast_8: tnk_ballast[8,1] <= 0
 lowerboundBallast_8: tnk_ballast[8,2] >= 0
 upperboundBallast_8: tnk_ballast[8,2] <= 0
 lowerboundBallast_8: tnk_ballast[8,3] >= 0
 upperboundBallast_8: tnk_ballast[8,3] <= 0
 lowerboundBallast_9: tnk_ballast[9,1] >= 0
 upperboundBallast_9: tnk_ballast[9,1] <= 0
 lowerboundBallast_9: tnk_ballast[9,2] >= 0
 upperboundBallast_9: tnk_ballast[9,2] <= 0
 lowerboundBallast_9: tnk_ballast[9,3] >= 0
 upperboundBallast_9: tnk_ballast[9,3] <= 0
 lowerboundBallast_10: tnk_ballast[10,1] >= 0
 upperboundBallast_10: tnk_ballast[10,1] <= 0
 lowerboundBallast_10: tnk_ballast[10,2] >= 0
 upperboundBallast_10: tnk_ballast[10,2] <= 0
 lowerboundBallast_10: tnk_ballast[10,3] >= 0
 upperboundBallast_10: tnk_ballast[10,3] <= 0
 lowerboundBallast_11: tnk_ballast[11,1] >= 0
 upperboundBallast_11: tnk_ballast[11,1] <= 0
 lowerboundBallast_11: tnk_ballast[11,2] >= 0
 upperboundBallast_11: tnk_ballast[11,2] <= 0
 lowerboundBallast_11: tnk_ballast[11,3] >= 0
 upperboundBallast_11: tnk_ballast[11,3] <= 0
 lowerboundBallast_12: tnk_ballast[12,1] >= 0
 upperboundBallast_12: tnk_ballast[12,1] <= 0
 lowerboundBallast_12: tnk_ballast[12,2] >= 0
 upperboundBallast_12: tnk_ballast[12,2] <= 0
 lowerboundBallast_12: tnk_ballast[12,3] >= 0
 upperboundBallast_12: tnk_ballast[12,3] <= 0
 lowerboundBallast_13: tnk_ballast[13,1] >= 0
 upperboundBallast_13: tnk_ballast[13,1] <= 0
 lowerboundBallast_13: tnk_ballast[13,2] >= 0
 upperboundBallast_13: tnk_ballast[13,2] <= 0
 lowerboundBallast_13: tnk_ballast[13,3] >= 0
 upperboundBallast_13: tnk_ballast[13,3] <= 0
 lowerboundBallast_14: tnk_ballast[14,1] >= 0
 upperboundBallast_14: tnk_ballast[14,1] <= 0
 lowerboundBallast_14: tnk_ballast[14,2] >= 0
 upperboundBallast_14: tnk_ballast[14,2] <= 0
 lowerboundBallast_14: tnk_ballast[14,3] >= 0
 upperboundBallast_14: tnk_ballast[14,3] <= 0
 maxqtyAll: X[1,1,1,2] + X[2,1,1,2] + X[3,1,1,2] + X[4,1,1,2] + X[5,1,1,2]
   <= 33000
 minqtyall: X[1,1,1,2] + X[2,1,1,2] + X[3,1,1,2] + X[4,1,1,2] + X[5,1,1,2]
   >= 27000
 yy: 1.15606936416185 X[1,1,1,1] + 1.128668171557562 X[1,1,1,2]
   + 1.15606936416185 X[1,2,1,1] + 1.128668171557562 X[1,2,1,2] <= 20272
 yy: 1.15606936416185 X[2,1,1,1] + 1.128668171557562 X[2,1,1,2]
   + 1.15606936416185 X[2,2,1,1] + 1.128668171557562 X[2,2,1,2] <= 23881
 yy: 1.15606936416185 X[3,1,1,1] + 1.128668171557562 X[3,1,1,2]
   + 1.15606936416185 X[3,2,1,1] + 1.128668171557562 X[3,2,1,2] <= 21509
 yy: 1.15606936416185 X[4,1,1,1] + 1.128668171557562 X[4,1,1,2]
   + 1.15606936416185 X[4,2,1,1] + 1.128668171557562 X[4,2,1,2] <= 23886
 yy: 1.15606936416185 X[5,1,1,1] + 1.128668171557562 X[5,1,1,2]
   + 1.15606936416185 X[5,2,1,1] + 1.128668171557562 X[5,2,1,2] <= 20676
 ww: X[1,1,1,1] + X[1,1,1,2] + X[1,2,1,1] + X[1,2,1,2] <= 20894
 ww: X[2,1,1,1] + X[2,1,1,2] + X[2,2,1,1] + X[2,2,1,2] <= 23912
 ww: X[3,1,1,1] + X[3,1,1,2] + X[3,2,1,1] + X[3,2,1,2] <= 21445
 ww: X[4,1,1,1] + X[4,1,1,2] + X[4,2,1,1] + X[4,2,1,2] <= 23933
 ww: X[5,1,1,1] + X[5,1,1,2] + X[5,2,1,1] + X[5,2,1,2] <= 20816
Bounds
Binaries
 B[1,1,1,1] B[1,1,1,2] B[1,2,1,1] B[1,2,1,2] B[1,3,1,1] B[1,3,1,2]
 B[1,4,1,1] B[1,4,1,2] B[2,1,1,1] B[2,1,1,2] B[2,2,1,1] B[2,2,1,2]
 B[2,3,1,1] B[2,3,1,2] B[2,4,1,1] B[2,4,1,2] B[3,1,1,1] B[3,1,1,2]
 B[3,2,1,1] B[3,2,1,2] B[3,3,1,1] B[3,3,1,2] B[3,4,1,1] B[3,4,1,2]
 B[4,1,1,1] B[4,1,1,2] B[4,2,1,1] B[4,2,1,2] B[4,3,1,1] B[4,3,1,2]
 B[4,4,1,1] B[4,4,1,2] B[5,1,1,1] B[5,1,1,2] B[5,2,1,1] B[5,2,1,2]
 B[5,3,1,1] B[5,3,1,2] B[5,4,1,1] B[5,4,1,2] adjcargo2[1,1,1,1]
 adjcargo2[1,1,1,2] adjcargo2[1,2,1,1] adjcargo2[1,2,1,2]
 adjcargo2[1,3,1,1] adjcargo2[1,3,1,2] adjcargo2[1,4,1,1]
 adjcargo2[1,4,1,2] adjcargo2[2,1,1,1] adjcargo2[2,1,1,2]
 adjcargo2[2,2,1,1] adjcargo2[2,2,1,2] adjcargo2[2,3,1,1]
 adjcargo2[2,3,1,2] adjcargo2[2,4,1,1] adjcargo2[2,4,1,2]
 adjcargo2[3,1,1,1] adjcargo2[3,1,1,2] adjcargo2[3,2,1,1]
 adjcargo2[3,2,1,2] adjcargo2[3,3,1,1] adjcargo2[3,3,1,2]
 adjcargo2[3,4,1,1] adjcargo2[3,4,1,2] adjcargo2[4,1,1,1]
 adjcargo2[4,1,1,2] adjcargo2[4,2,1,1] adjcargo2[4,2,1,2]
 adjcargo2[4,3,1,1] adjcargo2[4,3,1,2] adjcargo2[4,4,1,1]
 adjcargo2[4,4,1,2] b_holdasballast[1,1] b_holdasballast[2,1]
 b_holdasballast[3,1] cb_hold[1,1] cb_hold[2,1] cb_hold[3,1]
End
