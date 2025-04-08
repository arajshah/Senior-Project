from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from models.community import ForumTopic, ForumPost, SupportGroup, Event, GroupMembership
from models.user import User
from db import db
from datetime import datetime, timedelta
import random

community_bp = Blueprint('community_bp', __name__)

# Sample data - would normally be in database
sample_topics = [
    {
        'id': 1,
        'title': 'Coping with Anxiety',
        'description': 'Share your experiences and tips for managing anxiety.',
        'author': {'id': 2, 'name': 'Emily Chen', 'avatar': 'avatar-2.jpg'},
        'created_at': datetime.now() - timedelta(days=5),
        'post_count': 24,
        'last_activity': datetime.now() - timedelta(hours=3)
    },
    {
        'id': 2,
        'title': 'Depression Support',
        'description': 'A safe space to discuss depression and support each other.',
        'author': {'id': 3, 'name': 'Marcus Johnson', 'avatar': 'avatar-3.jpg'},
        'created_at': datetime.now() - timedelta(days=10),
        'post_count': 42,
        'last_activity': datetime.now() - timedelta(hours=1)
    },
    {
        'id': 3,
        'title': 'Mindfulness Practices',
        'description': 'Share and discuss mindfulness techniques and experiences.',
        'author': {'id': 4, 'name': 'Sophia Williams', 'avatar': 'avatar-4.jpg'},
        'created_at': datetime.now() - timedelta(days=3),
        'post_count': 15,
        'last_activity': datetime.now() - timedelta(hours=6)
    },
    {
        'id': 4,
        'title': 'Work-Life Balance',
        'description': 'Strategies for maintaining mental health while balancing work demands.',
        'author': {'id': 5, 'name': 'David Lee', 'avatar': 'avatar-5.jpg'},
        'created_at': datetime.now() - timedelta(days=7),
        'post_count': 31,
        'last_activity': datetime.now() - timedelta(hours=12)
    },
    {
        'id': 5,
        'title': 'Positive Psychology',
        'description': 'Focusing on strengths, positivity, and personal growth.',
        'author': {'id': 6, 'name': 'Olivia Taylor', 'avatar': 'avatar-6.jpg'},
        'created_at': datetime.now() - timedelta(days=4),
        'post_count': 19,
        'last_activity': datetime.now() - timedelta(hours=8)
    }
]

sample_posts = [{
        'id': 1,
        'topic_id': 1,
        'author': {'id': 2, 'name': 'Emily Chen', 'avatar': 'avatar-2.jpg'},
        'content': "I've found that deep breathing exercises help me manage my anxiety in the moment. What techniques work for you?",
        'created_at': datetime.now() - timedelta(days=5),
        'likes': 18
}, 
{
        'id': 2,
        'topic_id': 1,
        'author': {'id': 7, 'name': 'James Wilson', 'avatar': 'avatar-7.jpg'},
        'content': 'Mindfulness meditation has been life-changing for me. I try to practice for 10 minutes every morning, and it really helps set a calm tone for the day.',
        'created_at': datetime.now() - timedelta(days=5, hours=2),
        'likes': 12
},
{
    'id': 3,
    'topic_id': 1,
    'author': {'id': 3, 'name': 'Marcus Johnson', 'avatar': 'avatar-3.jpg'},
    'content': "I've been using the 5-4-3-2-1 grounding technique when I feel an anxiety attack coming on. You focus on 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste.",
    'created_at': datetime.now() - timedelta(days=4),
    'likes': 24
},
{
    'id': 4,
    'topic_id': 1,
    'author': {'id': 8, 'name': 'Aisha Patel', 'avatar': 'avatar-8.jpg'},
    'content': "Exercise has been my best anxiety management tool. Even a 15-minute walk can make a huge difference when I'm feeling overwhelmed.",
    'created_at': datetime.now() - timedelta(days=3, hours=5),
    'likes': 9
},
{
    'id': 5,
    'topic_id': 1,
    'author': {'id': 4, 'name': 'Sophia Williams', 'avatar': 'avatar-4.jpg'},
    'content': "I recently started journaling about my anxiety triggers, and it's helping me identify patterns I wasn't aware of before. Has anyone else tried this?",
    'created_at': datetime.now() - timedelta(hours=20),
    'likes': 5
}]

sample_groups = [
    {
        'id': 1,
        'name': 'Anxiety Support Circle',
        'description': 'A supportive community for those dealing with anxiety disorders.',
        'image': 'group-anxiety.jpg',
        'member_count': 156,
        'meeting_frequency': 'Weekly - Mondays at 7:00 PM',
        'next_meeting': datetime.now() + timedelta(days=(7 - datetime.now().weekday()) % 7),  # Next Monday
        'facilitator': 'Dr. Sarah Johnson',
        'max_participants': 200,
        'created_at': datetime.now() - timedelta(days=365),
        'meeting_link': 'https://zoom.us/j/123456789'
    },
    {
        'id': 2,
        'name': 'Depression Recovery',
        'description': 'Support and encouragement for those on the journey to recovery from depression.',
        'image': 'group-depression.jpg',
        'member_count': 142,
        'meeting_frequency': 'Weekly - Wednesdays at 6:30 PM',
        'next_meeting': datetime.now() + timedelta(days=(9 - datetime.now().weekday()) % 7),  # Next Wednesday
        'facilitator': 'Dr. Michael Rodriguez',
        'max_participants': 150,
        'created_at': datetime.now() - timedelta(days=300),
        'meeting_link': 'https://zoom.us/j/987654321'
    },
    {
        'id': 3,
        'name': 'Mindfulness Meditation',
        'description': 'Practice mindfulness techniques together and discuss their benefits for mental health.',
        'image': 'group-mindfulness.jpg',
        'member_count': 98,
        'meeting_frequency': 'Bi-weekly - Fridays at 6:00 PM',
        'next_meeting': datetime.now() + timedelta(days=(11 - datetime.now().weekday()) % 14),  # Next Friday or after
        'facilitator': 'Emma Thompson, Meditation Instructor',
        'max_participants': 120,
        'created_at': datetime.now() - timedelta(days=180),
        'meeting_link': 'https://zoom.us/j/456789123'
    },
    {
        'id': 4,
        'name': 'Grief and Loss',
        'description': 'Find comfort and understanding as we navigate the complex emotions of grief together.',
        'image': 'group-grief.jpg',
        'member_count': 78,
        'meeting_frequency': 'Weekly - Thursdays at 7:30 PM',
        'next_meeting': datetime.now() + timedelta(days=(10 - datetime.now().weekday()) % 7),  # Next Thursday
        'facilitator': 'Robert Martinez, Grief Counselor',
        'max_participants': 100,
        'created_at': datetime.now() - timedelta(days=245),
        'meeting_link': 'https://zoom.us/j/321654987'
    },
    {
        'id': 5,
        'name': 'LGBTQ+ Mental Health',
        'description': 'A safe space for LGBTQ+ individuals to discuss mental health challenges and experiences.',
        'image': 'group-lgbtq.jpg',
        'member_count': 112,
        'meeting_frequency': 'Weekly - Tuesdays at 7:00 PM',
        'next_meeting': datetime.now() + timedelta(days=(8 - datetime.now().weekday()) % 7),  # Next Tuesday
        'facilitator': 'Alex Patel, LCSW',
        'max_participants': 150,
        'created_at': datetime.now() - timedelta(days=275),
        'meeting_link': 'https://zoom.us/j/159753456'
    }
]

sample_events = [
    {
        'id': 1,
        'title': 'Stress Management Workshop',
        'description': 'Learn effective strategies to manage stress in your daily life with Dr. Sarah Cohen.',
        'image': 'event-stress.jpg',
        'date': datetime.now() + timedelta(days=5),
        'time': '10:00 AM - 12:00 PM',
        'location': 'Virtual (Zoom)',
        'organizer': 'Aurora Mental Health Team',
        'attendee_count': 42,
        'duration_minutes': 120,
        'host': 'Dr. Sarah Cohen',
        'meeting_link': 'https://zoom.us/j/123456789',
        'recording_link': None,
        'attendees': [
            {'id': 2, 'username': 'Emily Chen'},
            {'id': 3, 'username': 'Marcus Johnson'},
            {'id': 7, 'username': 'James Wilson'},
            {'id': 8, 'username': 'Aisha Patel'}
        ]
    },
    {
        'id': 2,
        'title': 'Mindfulness Meditation Session',
        'description': 'Join us for a guided mindfulness meditation session led by certified instructor Michael Chen.',
        'image': 'event-meditation.jpg',
        'date': datetime.now() + timedelta(days=2),
        'time': '6:30 PM - 7:30 PM',
        'location': 'Virtual (Zoom)',
        'organizer': 'Mindfulness Meditation Group',
        'attendee_count': 67,
        'duration_minutes': 60,
        'host': 'Michael Chen',
        'meeting_link': 'https://zoom.us/j/987654321',
        'recording_link': None,
        'attendees': [
            {'id': 2, 'username': 'Emily Chen'},
            {'id': 4, 'username': 'Sophia Williams'},
            {'id': 5, 'username': 'David Lee'}
        ]
    },
    {
        'id': 3,
        'title': 'Understanding Anxiety Disorders',
        'description': 'Educational webinar about different types of anxiety disorders, symptoms, and treatment options.',
        'image': 'event-anxiety.jpg',
        'date': datetime.now() + timedelta(days=8),
        'time': '7:00 PM - 8:30 PM',
        'location': 'Virtual (Zoom)',
        'organizer': 'Dr. Emma Harris, Clinical Psychologist',
        'attendee_count': 89,
        'duration_minutes': 90,
        'host': 'Dr. Emma Harris',
        'meeting_link': 'https://zoom.us/j/456789123',
        'recording_link': None,
        'attendees': [
            {'id': 3, 'username': 'Marcus Johnson'},
            {'id': 6, 'username': 'Olivia Taylor'},
            {'id': 8, 'username': 'Aisha Patel'}
        ]
    },
    {
        'id': 4,
        'title': 'Art Therapy Workshop',
        'description': 'Express yourself through art in this therapeutic workshop. No artistic experience necessary.',
        'image': 'event-art.jpg',
        'date': datetime.now() + timedelta(days=12),
        'time': '2:00 PM - 4:00 PM',
        'location': 'Virtual (Zoom)',
        'organizer': 'Creative Healing Collective',
        'attendee_count': 35,
        'duration_minutes': 120,
        'host': 'Isabella Martinez',
        'meeting_link': 'https://zoom.us/j/321654987',
        'recording_link': None,
        'attendees': [
            {'id': 4, 'username': 'Sophia Williams'},
            {'id': 7, 'username': 'James Wilson'}
        ]
    },
    {
        'id': 5,
        'title': 'Coping with Grief and Loss',
        'description': 'A supportive session for those experiencing grief, with guidance from grief counselor Robert Martinez.',
        'image': 'event-grief.jpg',
        'date': datetime.now() - timedelta(days=7),  # Past event
        'time': '6:00 PM - 7:30 PM',
        'location': 'Virtual (Zoom)',
        'organizer': 'Grief and Loss Support Group',
        'attendee_count': 28,
        'duration_minutes': 90,
        'host': 'Robert Martinez',
        'meeting_link': None,
        'recording_link': 'https://zoom.us/rec/share/sample-recording-link',
        'attendees': [
            {'id': 2, 'username': 'Emily Chen'},
            {'id': 5, 'username': 'David Lee'},
            {'id': 6, 'username': 'Olivia Taylor'}
        ]
    }
]


@community_bp.route('/community')
def community_home():
    # Get sample trending topics, upcoming events, and featured groups
    trending_topics = random.sample(sample_topics, min(3, len(sample_topics)))
    upcoming_events = sorted(sample_events, key=lambda e: e['date'])[:3]
    featured_groups = random.sample(sample_groups, min(3, len(sample_groups)))
    
    return render_template('community/community_home.html', 
                          trending_topics=trending_topics,
                          upcoming_events=upcoming_events,
                          featured_groups=featured_groups)


@community_bp.route('/community/forums')
def forums():
    # Get all forum topics
    topics = sample_topics
    
    return render_template('community/forums.html', topics=topics)


@community_bp.route('/community/forums/detail/<int:topic_id>')
def forum_detail(topic_id):
    # Get topic and its posts
    topic = next((t for t in sample_topics if t['id'] == topic_id), None)
    
    if not topic:
        flash('Topic not found', 'error')
        return redirect(url_for('community_bp.forums'))
    
    # Get posts for this topic
    posts = [p for p in sample_posts if p['topic_id'] == topic_id]
    
    return render_template('community/forum_detail.html', topic=topic, posts=posts)


@community_bp.route('/community/groups')
def groups():
    # Get all support groups
    return render_template('community/groups.html', groups=sample_groups)


@community_bp.route('/community/groups/<int:group_id>')
def group_detail(group_id):
    # Get group details
    group = next((g for g in sample_groups if g['id'] == group_id), None)
    
    if not group:
        flash('Group not found', 'error')
        return redirect(url_for('community_bp.groups'))
    
    # Sample members for display with username field
    members = [
        {'id': 2, 'username': 'Emily Chen', 'avatar': 'avatar-2.jpg'},
        {'id': 3, 'username': 'Marcus Johnson', 'avatar': 'avatar-3.jpg'},
        {'id': 4, 'username': 'Sophia Williams', 'avatar': 'avatar-4.jpg'},
        {'id': 7, 'username': 'James Wilson', 'avatar': 'avatar-7.jpg'},
        {'id': 8, 'username': 'Aisha Patel', 'avatar': 'avatar-8.jpg'}
    ]
    
    # Determine if current user is a member
    user_id = session.get('user_id')
    is_member = user_id and (user_id in [m['id'] for m in members])
    
    # Create user_groups list for checking if the user is a member
    user_groups = []
    if user_id:
        # In a real app, this would come from the database
        # For now, if is_member is True, add this group to user_groups
        if is_member:
            user_groups.append(group)
    
    return render_template('community/group_detail.html', 
                          group=group, 
                          members=members,  # Show all members
                          is_member=is_member,
                          user_groups=user_groups,
                          timedelta=timedelta)


@community_bp.route('/community/events')
def events():
    # Get all events
    upcoming_events = sorted([e for e in sample_events if e['date'] >= datetime.now()], 
                           key=lambda e: e['date'])
    
    return render_template('community/events.html', events=upcoming_events)


@community_bp.route('/community/events/<int:event_id>')
def event_detail(event_id):
    # Get event details
    event = next((e for e in sample_events if e['id'] == event_id), None)
    
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('community_bp.events'))
    
    # Check if user is registered
    user_id = session.get('user_id')
    is_registered = user_id and (user_id in [a['id'] for a in event['attendees']])
    
    # Create user_events list for checking if the user registered
    user_events = []
    if user_id:
        # In a real app, this would come from the database
        # For now, if is_registered is True, add this event to user_events
        if is_registered:
            user_events.append(event)
    
    # Get related events (same category or similar)
    related_events = [e for e in sample_events if e['id'] != event_id]
    related_events = random.sample(related_events, min(2, len(related_events)))
    
    # Convert string time to datetime object for template
    event_datetime = event['date']
    
    return render_template('community/event_detail.html', 
                          event=event, 
                          is_registered=is_registered,
                          related_events=related_events,
                          user_events=user_events,
                          now=datetime.now())


@community_bp.route('/community/join-group/<int:group_id>', methods=['POST'])
def join_group(group_id):
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'You must be logged in to join a group'}), 401
    
    # In a real app, would add the user to the group in the database
    return jsonify({'success': True, 'message': 'Successfully joined the group'})


@community_bp.route('/community/leave-group/<int:group_id>', methods=['POST'])
def leave_group(group_id):
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'You must be logged in to leave a group'}), 401
    
    # In a real app, would remove the user from the group in the database
    return jsonify({'success': True, 'message': 'Successfully left the group'})


@community_bp.route('/community/register-event/<int:event_id>', methods=['POST'])
def register_event(event_id):
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'You must be logged in to register for an event'}), 401
    
    # In a real app, would add the user to the event in the database
    return jsonify({'success': True, 'message': 'Successfully registered for the event'})


@community_bp.route('/community/cancel-registration/<int:event_id>', methods=['POST'])
def cancel_registration(event_id):
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'You must be logged in to cancel registration'}), 401
    
    # In a real app, would remove the user from the event in the database
    return jsonify({'success': True, 'message': 'Registration successfully canceled'})


@community_bp.route('/community/post-reply/<int:topic_id>', methods=['POST'])
def post_reply(topic_id):
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'You must be logged in to post a reply'}), 401
    
    content = request.json.get('content')
    if not content:
        return jsonify({'success': False, 'message': 'Reply content cannot be empty'}), 400
    
    # In a real app, would add the reply to the database
    # Here we're just returning success
    return jsonify({'success': True, 'message': 'Reply posted successfully'})