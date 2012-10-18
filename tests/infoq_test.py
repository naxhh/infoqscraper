import datetime
import pprint
import tempfile
import os
import unittest2
import infoq

try:
    USERNAME = os.environ['INFOQ_USERNAME']
except KeyError:
    USERNAME = None

try:
    PASSWORD = os.environ['INFOQ_PASSWORD']
except  KeyError:
    PASSWORD = None


class TestInfoQ(unittest2.TestCase):
    def setUp(self):
        self.iq = infoq.InfoQ()

    @property
    def latest_presentation(self):
        ps = self.iq.presentation_summaries().next()
        return infoq.Presentation(ps['id'])

    def assertValidPresentationMetadata(self, m):
        self.assertEqual(len(m), 12)

        self.assertIsInstance(m['title'], basestring)
        self.assertIsInstance(m['date'],  datetime.datetime)
        self.assertIsInstance(m['duration'], int)
        self.assertIsInstance(m['sections'], list)
        for s in m['sections']:
            self.assertIsInstance(s, basestring)
        self.assertIsInstance(m['topics'], list)
        for s in m['topics']:
            self.assertIsInstance(s, basestring)
        self.assertIsInstance(m['summary'], basestring)
        self.assertIsInstance(m['bio'], basestring)
        self.assertIsInstance(m['about'], basestring)
        self.assertIsInstance(m['timecodes'], list)
        prev = -1
        for t in m['timecodes']:
            self.assertIsInstance(t, int)
            self.assertGreater(t, prev)
            prev = t
        self.assertIsInstance(m['slides'], list)
        for s in m['slides']:
            self.assertIsInstance(s, basestring)
            #self.assertTrue(s.startswith("http://"))
        self.assertIsInstance(m['video'], basestring)
        self.assertTrue(m['video'].startswith("rtmpe://"))

    def test_login_ok(self):
        if USERNAME and PASSWORD:
            self.iq._login(USERNAME, PASSWORD)

    def test_login_fail(self):
        self.assertRaises(Exception, self.iq._login, "user", "password")

    def test_rightbar_summaries(self):
        for index in xrange(2):
            rb = infoq.RightBarPage(1)
            rb.fetch()

            count = 0
            for entry in rb.summaries():
                count += 1
                self.assertIsNotNone(entry['id'])
                self.assertIsNotNone(entry['path'])
                self.assertIsNotNone(entry['desc'])
                self.assertIsNotNone(entry['auth'])
                self.assertIsNotNone(entry['date'])
                self.assertIsNotNone(entry['title'])

            self.assertGreaterEqual(count, infoq.RIGHT_BAR_ENTRIES_PER_PAGES)

    def test_presentation_summaries(self):
        count = 0
        for entry in self.iq.presentation_summaries():
            count += 1
            if count > infoq.RIGHT_BAR_ENTRIES_PER_PAGES * 3:
                break

    def test_presentation_summaries_custom_func(self):
        # Check that only fetch one page
        count = 0
        for entry in self.iq.presentation_summaries(filter=infoq.MaxPagesFilter(1)):
            self.assertLessEqual(count, infoq.RIGHT_BAR_ENTRIES_PER_PAGES)
            count += 1

        self.assertEqual(count, infoq.RIGHT_BAR_ENTRIES_PER_PAGES)


    def test_presentation_java_gc_azul(self):
        p = infoq.Presentation("Java-GC-Azul-C4")

        self.assertValidPresentationMetadata(p.metadata)

        self.assertEqual(p.metadata['title'], "Understanding Java Garbage Collection and What You Can Do about It")
        self.assertEqual(p.metadata['date'], datetime.datetime(2012, 10, 17))
        self.assertEqual(p.metadata['auth'], "Gil Tene")
        self.assertEqual(p.metadata['duration'], 3469)
        self.assertEqual(p.metadata['sections'], ['Architecture & Design', 'Development'])
        self.assertItemsEqual(p.metadata['topics'], ['Azul Zing' , 'Azul' , 'JVM' , 'Virtual Machines' , 'Runtimes' , 'Java' , 'QCon New York 2012' , 'GarbageCollection' , 'QCon'])
        self.assertItemsEqual(p.metadata['summary'], "Gil Tene explains how a garbage collector works, covering the fundamentals, mechanism, terminology and metrics. He classifies several GCs, and introduces Azul C4.")
        self.assertEqual(p.metadata['bio'], "Gil Tene is CTO and co-founder of Azul Systems. He has been involved with virtual machine technologies for the past 20 years and has been building Java technology-based products since 1995. Gil pioneered Azul's Continuously Concurrent Compacting Collector (C4), Java Virtualization, Elastic Memory, and various managed runtime and systems stack technologies.")
        self.assertEqual(p.metadata['about'], 'Software is changing the world; QCon aims to empower software development by facilitating the spread of knowledge and innovation in the enterprise software development community; to achieve this, QCon is organized as a practitioner-driven conference designed for people influencing innovation in their teams: team leads, architects, project managers, engineering directors.')
        self.assertEqual(p.metadata['timecodes'], [3,15,73,143,227,259,343,349,540,629,752,755,822,913,1043,1210,1290,1360,1386,1462,1511,1633,1765,1892,1975,2009,2057,2111,2117,2192,2269,2328,2348,2468,2558,2655,2666,2670,2684,2758,2802,2820,2827,2838,2862,2913,2968,3015,3056,3076,3113,3115,3135,3183,3187,3247,3254,3281,3303,3328,3344,3360,3367,3376,3411,3426,3469])
        self.assertEqual(p.metadata['slides'], ['/resource/presentations/Java-GC-Azul-C4/en/slides/1.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/2.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/3.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/4.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/5.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/6.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/7.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/8.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/9.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/10.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/11.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/12.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/13.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/14.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/15.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/16.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/17.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/18.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/19.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/20.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/21.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/22.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/23.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/24.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/25.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/26.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/27.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/28.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/29.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/30.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/31.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/32.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/33.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/34.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/35.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/36.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/37.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/38.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/39.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/40.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/41.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/42.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/43.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/44.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/45.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/46.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/47.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/48.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/50.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/52.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/55.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/56.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/57.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/58.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/59.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/60.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/61.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/62.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/63.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/64.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/66.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/67.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/68.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/69.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/70.swf','/resource/presentations/Java-GC-Azul-C4/en/slides/71.swf'])
        self.assertEqual(p.metadata['video'], "rtmpe://video.infoq.com/cfx/st/presentations/12-jun-everythingyoueverwanted.mp4")

    def test_fetch(self):
        tmp_dir = tempfile.mkdtemp()
        p = self.latest_presentation

        infoq.fetch([infoq.get_url(slide) for slide in p.metadata['slides']], tmp_dir)
        file_list = [os.path.join(tmp_dir, file) for file in os.listdir(tmp_dir)]
        self.assertEqual(len(file_list),  len(p.metadata['slides']))

        for file in file_list:
            stat_info = os.stat(file)
            self.assertGreater(stat_info.st_size, 1000)
            os.remove(file)
        os.rmdir(tmp_dir)

    def test_presentation_latest(self):
        p = self.latest_presentation
        pprint.pprint(p.metadata)
        self.assertValidPresentationMetadata(p.metadata)


if __name__ == '__main__':
    unittest2.main()
