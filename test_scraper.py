import tempfile
import unittest
from datetime import date
from pathlib import Path
from scraper import result_date, merge_and_save, read_existing_csv, results_url

class Tests(unittest.TestCase):
    def test_league_urls(self):
        self.assertEqual(results_url('https://www.flashscore.com/basketball/australia/nbl/'),
                         'https://www.flashscore.com/basketball/australia/nbl/results/')
        for url in ['https://evil.com/basketball/australia/nbl/', 'https://www.flashscore.com/football/australia/nbl/']:
            with self.assertRaises(ValueError):
                results_url(url)

    def test_no_new_games_does_not_rewrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'games.csv'
            path.write_text('match_id,notes,custom\nold,keep,extra\n', encoding='utf-8')
            before = path.read_bytes()
            merge_and_save(path, [{'match_id': 'old', 'notes': 'replace'}])
            self.assertEqual(path.read_bytes(), before)
            merge_and_save(path, [{'match_id': 'new'}, {'match_id': 'new'}])
            rows = read_existing_csv(path)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows['old']['custom'], 'extra')
            self.assertEqual(rows['old']['notes'], 'keep')

    def test_invalid_csv_is_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'games.csv'
            path.write_text('team,score\nexample,80\n')
            before = path.read_bytes()
            with self.assertRaises(ValueError):
                merge_and_save(path, [])
            self.assertEqual(path.read_bytes(), before)

    def test_dates(self):
        self.assertEqual(result_date('08.10. 19:00', date(2026,10,9)), date(2026,10,8))
        self.assertEqual(result_date('31.12. 19:00', date(2027,1,2)), date(2026,12,31))
        self.assertEqual(result_date('08.10.2025 19:00', date(2026,10,9)), date(2025,10,8))
        self.assertIsNone(result_date('unknown', date(2026,10,9)))

    def test_upsert_preserves_notes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'games.csv'
            merge_and_save(path, [{'match_id':'one', 'home_total':'80'}])
            rows = read_existing_csv(path)
            rows['one']['notes'] = 'my note'
            import csv
            from scraper import RAW_FIELDS
            with path.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=RAW_FIELDS)
                writer.writeheader(); writer.writerows(rows.values())
            merged = merge_and_save(path, [{'match_id':'one', 'home_total':'81'}, {'match_id':'two'}])
            self.assertEqual(len(merged), 2)
            self.assertEqual(merged[0]['notes'], 'my note')
            self.assertEqual(merged[0]['home_total'], '80')

if __name__ == '__main__':
    unittest.main()
