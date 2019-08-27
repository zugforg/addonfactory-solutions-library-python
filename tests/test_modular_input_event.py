import sys
import os.path as op
import json

sys.path.insert(0, op.dirname(op.dirname(op.abspath(__file__))))
from solnlib.modular_input import XMLEvent
from solnlib.modular_input import HECEvent


def to_sorted_json_string(obj):
    return json.dumps(json.loads(str(obj)), sort_keys=True)


class TestXMLEvent(object):

    @classmethod
    def setup_class(cls):
        cls.xe1 = XMLEvent(data='This is a test data1.',
                           time=1372274622.493,
                           index='main',
                           host='localhost',
                           source='Splunk',
                           sourcetype='misc',
                           stanza='test_scheme://test',
                           unbroken=True,
                           done=False)

        cls.xe2 = XMLEvent(data='This is a test data2.',
                           time=1372274622.493,
                           index='main',
                           host='localhost',
                           source='Splunk',
                           sourcetype='misc',
                           stanza='test_scheme://test',
                           unbroken=True,
                           done=True)

        cls.xe3 = XMLEvent(data='This is a test data3.',
                           time=1372274622.493,
                           index='main',
                           host='localhost',
                           source='Splunk',
                           sourcetype='misc',
                           stanza='test_scheme://test')

        cls.xe4 = XMLEvent(data=u'This is utf-8 \u2603 data4.',
                           time=1372274622.493,
                           index='main',
                           host='localhost',
                           source='Splunk',
                           sourcetype='misc',
                           stanza='test_scheme://test')

    def test_str(self, monkeypatch):
        assert to_sorted_json_string(self.xe1) == '{"data": "This is a test data1.", "done": false, "host": "localhost", "index": "main", "source": "Splunk", "sourcetype": "misc", "stanza": "test_scheme://test", "time": 1372274622.493, "unbroken": true}'
        assert to_sorted_json_string(self.xe2) == '{"data": "This is a test data2.", "done": true, "host": "localhost", "index": "main", "source": "Splunk", "sourcetype": "misc", "stanza": "test_scheme://test", "time": 1372274622.493, "unbroken": true}'
        assert to_sorted_json_string(self.xe3) == '{"data": "This is a test data3.", "done": false, "host": "localhost", "index": "main", "source": "Splunk", "sourcetype": "misc", "stanza": "test_scheme://test", "time": 1372274622.493, "unbroken": false}'

    def test_format_events(self, monkeypatch):
        assert XMLEvent.format_events([self.xe1, self.xe2]) == ['<stream><event stanza="test_scheme://test" unbroken="1"><time>1372274622.493</time><index>main</index><host>localhost</host><source>Splunk</source><sourcetype>misc</sourcetype><data>This is a test data1.</data></event><event stanza="test_scheme://test" unbroken="1"><time>1372274622.493</time><index>main</index><host>localhost</host><source>Splunk</source><sourcetype>misc</sourcetype><data>This is a test data2.</data><done /></event></stream>']
        assert XMLEvent.format_events([self.xe3]) == ['<stream><event stanza="test_scheme://test"><time>1372274622.493</time><index>main</index><host>localhost</host><source>Splunk</source><sourcetype>misc</sourcetype><data>This is a test data3.</data></event></stream>']
        assert XMLEvent.format_events([self.xe4]) == [u'<stream><event stanza="test_scheme://test"><time>1372274622.493</time><index>main</index><host>localhost</host><source>Splunk</source><sourcetype>misc</sourcetype><data>This is utf-8 \u2603 data4.</data></event></stream>']


class TestHECEvent(object):

    @classmethod
    def setup_class(cls):
        cls.he1 = HECEvent(data='This is a test data1.',
                           time=1372274622.493,
                           index='main',
                           host='localhost',
                           source='Splunk',
                           sourcetype='misc',
                           stanza='test_scheme://test',
                           unbroken=True,
                           done=False)

        cls.he2 = HECEvent(data='This is a test data2.',
                           time=1372274622.493,
                           index='main',
                           host='localhost',
                           source='Splunk',
                           sourcetype='misc',
                           stanza='test_scheme://test',
                           unbroken=True,
                           done=True)

        cls.he3 = HECEvent(data='This is a test data3.',
                           time=1372274622.493,
                           index='main',
                           host='localhost',
                           source='Splunk',
                           sourcetype='misc',
                           stanza='test_scheme://test')

    def test_str(self, monkeypatch):
        assert to_sorted_json_string(self.he1) == '{"data": "This is a test data1.", "done": false, "host": "localhost", "index": "main", "source": "Splunk", "sourcetype": "misc", "stanza": "test_scheme://test", "time": 1372274622.493, "unbroken": true}'
        assert to_sorted_json_string(self.he2) == '{"data": "This is a test data2.", "done": true, "host": "localhost", "index": "main", "source": "Splunk", "sourcetype": "misc", "stanza": "test_scheme://test", "time": 1372274622.493, "unbroken": true}'
        assert to_sorted_json_string(self.he3) == '{"data": "This is a test data3.", "done": false, "host": "localhost", "index": "main", "source": "Splunk", "sourcetype": "misc", "stanza": "test_scheme://test", "time": 1372274622.493, "unbroken": false}'

    def test_format_events(self, monkeypatch):
        formatted_events = HECEvent.format_events([self.he1, self.he2])
        assert len(formatted_events) == 1

        event_strings = [to_sorted_json_string(e) for e in formatted_events[0].split('\n')]
        assert len(event_strings) == 2
        assert event_strings[0] == '{"event": "This is a test data1.", "host": "localhost", "index": "main", "source": "Splunk", "sourcetype": "misc", "time": 1372274622.493}'
        assert event_strings[1] == '{"event": "This is a test data2.", "host": "localhost", "index": "main", "source": "Splunk", "sourcetype": "misc", "time": 1372274622.493}'

        formatted_events = HECEvent.format_events([self.he3]) 
        assert len(formatted_events) == 1

        event_strings = [to_sorted_json_string(e) for e in formatted_events[0].split('\n')]
        assert len(event_strings) == 1
        assert event_strings[0] == '{"event": "This is a test data3.", "host": "localhost", "index": "main", "source": "Splunk", "sourcetype": "misc", "time": 1372274622.493}'
