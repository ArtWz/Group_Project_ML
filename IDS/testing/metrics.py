import sys

def calculateMetrics(tp, fp, tn, fn):

    print("True positives:", tp)
    print("False positives:", fp)
    print("True negatives:", tn)
    print("False negatives:", fn)

    if (tp + fp == 0):
        print("Precision: NaN (no positive predictions)")

        recall = tp / (tp + fn)
        print("Recall:", recall)

        print("F1 score: NaN (precision is NaN)")
    else:
        precision = tp / (tp + fp)
        print("Precision:", precision)

        recall = tp / (tp + fn)
        print("Recall:", recall)

        f1 = 2 * precision * recall / (precision + recall)
        print("F1 score:", f1)

print("\n")

# Normal
tp_normal = int(sys.argv[1])
fp_normal = int(sys.argv[2])
tn_normal = int(sys.argv[3])
fn_normal = int(sys.argv[4])

print("Category: Normal")
calculateMetrics(tp_normal, fp_normal, tn_normal, fn_normal)
print("\n")

# DoS
tp_dos = int(sys.argv[5])
fp_dos = int(sys.argv[6])
tn_dos = int(sys.argv[7])
fn_dos = int(sys.argv[8])

print("Category: DoS")
calculateMetrics(tp_dos, fp_dos, tn_dos, fn_dos)
print("\n")

# R2L
tp_r2l = int(sys.argv[9])
fp_r2l = int(sys.argv[10])
tn_r2l = int(sys.argv[11])
fn_r2l = int(sys.argv[12])

print("Category: R2L")
calculateMetrics(tp_r2l, fp_r2l, tn_r2l, fn_r2l)
print("\n")

# Probing
tp_probing = int(sys.argv[13])
fp_probing = int(sys.argv[14])
tn_probing = int(sys.argv[15])
fn_probing = int(sys.argv[16])

print("Category: Probing")
calculateMetrics(tp_probing, fp_probing, tn_probing, fn_probing)
print("\n")

# Overall accuracy
accuracy = (tp_normal + tp_dos + tp_r2l + tp_probing) / (tp_normal + tp_dos + tp_r2l + tp_probing + fp_normal + fp_dos + fp_r2l + fp_probing)
print ("Overall accuracy:", accuracy)