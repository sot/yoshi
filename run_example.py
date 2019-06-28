from astropy.table import Table

from yoshi.yoshi import run_one_yoshi


def main():
    import argparse
    parser = argparse.ArgumentParser(description="yoshi")
    parser.add_argument('jobreq', type=str)
    parser.add_argument('out', type=str)
    opt = parser.parse_args()
    obsjobs = Table.read(opt.jobreq, format='ascii')
    obsjob = obsjobs[0]
    rec = dict(zip(obsjob.colnames, obsjob))
    results = []
    for roll in range(0, 30):
        req = rec.copy()
        rec['roll_targ'] = roll
        report = run_one_yoshi(**req)
        results.append(report)
    Table(results).write(opt.out, format='ascii', overwrite=True)

if __name__ == '__main__':
    main()
