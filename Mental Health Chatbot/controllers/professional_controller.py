from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from datetime import datetime, timedelta
from flask import url_for
import random

professional_bp = Blueprint('professional_bp', __name__)

# Sample data for professionals
psychologists = [
    {
        'id': 1,
        'name': 'Dr. Emma Bennett',
        'title': 'Clinical Psychologist',
        'photo': "emma-bennett.jpg",
        'specialty': 'Anxiety, Depression, Trauma',
        'experience': '12 years',
        'rating': 4.9,
        'review_count': 124,
        'bio': 'Dr. Bennett specializes in cognitive-behavioral therapy and mindfulness-based approaches for anxiety disorders, depression, and trauma recovery. She has extensive training in EMDR for trauma treatment.',
        'education': [
            'Ph.D. in Clinical Psychology, Stanford University',
            'M.A. in Psychology, University of California, Berkeley',
            'B.A. in Psychology, UCLA'
        ],
        'approaches': [
            'Cognitive Behavioral Therapy (CBT)',
            'Mindfulness-Based Cognitive Therapy',
            'Eye Movement Desensitization and Reprocessing (EMDR)'
        ],
        'session_cost': '$150',
        'insurance': ['Aetna', 'Blue Cross', 'Cigna', 'UnitedHealthcare'],
        'languages': ['English', 'Spanish'],
        'video_intro': 'https://example.com/video/emma-bennett.mp4'
    },
    {
        'id': 2,
        'name': 'Dr. Marcus Rodriguez',
        'title': 'Clinical Psychologist',
        'photo': 'marcus-rodriguez.jpg',
        'specialty': 'Relationships, Life Transitions, LGBTQ+ Issues',
        'experience': '9 years',
        'rating': 4.8,
        'review_count': 98,
        'bio': 'Dr. Rodriguez helps clients navigate relationship challenges, major life transitions, and identity exploration. He provides a warm, affirming space for all clients, with particular expertise in LGBTQ+ issues.',
        'education': [
            'Psy.D. in Clinical Psychology, Rutgers University',
            'M.S. in Counseling Psychology, Columbia University',
            'B.S. in Psychology, NYU'
        ],
        'approaches': [
            'Psychodynamic Therapy',
            'Emotion-Focused Therapy',
            'Narrative Therapy',
            'Attachment-Based Therapy'
        ],
        'session_cost': '$140',
        'insurance': ['Blue Cross', 'Cigna', 'Optum', 'Oscar'],
        'languages': ['English', 'Portuguese'],
        'video_intro': 'https://example.com/video/marcus-rodriguez.mp4'
    },
    {
        'id': 3,
        'name': 'Dr. Sarah Chen',
        'title': 'Health Psychologist',
        'photo': 'sarah-chen.jpg',
        'specialty': 'Chronic Illness, Stress Management, Health Behavior Change',
        'experience': '15 years',
        'rating': 4.7,
        'review_count': 142,
        'bio': 'Dr. Chen specializes in helping clients manage chronic health conditions, reduce stress, and make sustainable health behavior changes. She integrates medical knowledge with psychological techniques to address the mind-body connection.',
        'education': [
            'Ph.D. in Health Psychology, University of Michigan',
            'M.S. in Public Health, Johns Hopkins University',
            'B.S. in Biopsychology, University of Washington'
        ],
        'approaches': [
            'Acceptance and Commitment Therapy (ACT)',
            'Biofeedback',
            'Motivational Interviewing',
            'Stress Management Training'
        ],
        'session_cost': '$160',
        'insurance': ['Aetna', 'Blue Cross', 'Cigna', 'Medicare'],
        'languages': ['English', 'Mandarin Chinese'],
        'video_intro': 'https://example.com/video/sarah-chen.mp4'
    },
    {
        'id': 4,
        'name': 'Dr. James Taylor',
        'title': 'Clinical Psychologist',
        'photo': 'james-taylor.jpg',
        'specialty': 'OCD, Phobias, Anxiety Disorders',
        'experience': '11 years',
        'rating': 4.9,
        'review_count': 107,
        'bio': 'Dr. Taylor specializes in evidence-based treatments for OCD, phobias, and anxiety disorders. He takes a structured approach to therapy, helping clients face fears and overcome limiting behaviors.',
        'education': [
            'Ph.D. in Clinical Psychology, University of Pennsylvania',
            'M.A. in Psychology, Boston University',
            'B.A. in Psychology, Brown University'
        ],
        'approaches': [
            'Exposure and Response Prevention (ERP)',
            'Cognitive Behavioral Therapy (CBT)',
            'Acceptance and Commitment Therapy (ACT)'
        ],
        'session_cost': '$155',
        'insurance': ['Aetna', 'Blue Cross', 'UnitedHealthcare', 'Humana'],
        'languages': ['English'],
        'video_intro': 'https://example.com/video/james-taylor.mp4'
    }
]

psychiatrists = [
    {
        'id': 5,
        'name': 'Dr. Olivia Washington',
        'title': 'Psychiatrist',
        'photo': 'olivia-washington.jpg',
        'specialty': 'Depression, Anxiety, Bipolar Disorder',
        'experience': '14 years',
        'rating': 4.8,
        'review_count': 132,
        'bio': 'Dr. Washington specializes in the evaluation, diagnosis, and medication management of mood and anxiety disorders. She takes a holistic approach, considering lifestyle factors and therapy alongside medication when appropriate.',
        'education': [
            'M.D., Johns Hopkins School of Medicine',
            'Psychiatry Residency, Massachusetts General Hospital',
            'B.S. in Neuroscience, Duke University'
        ],
        'approaches': [
            'Medication Management',
            'Integrative Psychiatry',
            'Psychopharmacology',
            'Collaborative Care'
        ],
        'session_cost': '$200',
        'insurance': ['Aetna', 'Blue Cross', 'Cigna', 'UnitedHealthcare', 'Medicare'],
        'languages': ['English'],
        'video_intro': 'https://example.com/video/olivia-washington.mp4'
    },
    {
        'id': 6,
        'name': 'Dr. Michael Patel',
        'title': 'Psychiatrist',
        'photo': 'michael-patel.jpg',
        'specialty': 'ADHD, Depression, Anxiety',
        'experience': '10 years',
        'rating': 4.7,
        'review_count': 98,
        'bio': 'Dr. Patel focuses on evidence-based psychiatric treatment for adults with ADHD, depression, and anxiety disorders. He believes in transparent conversations about medication options, benefits, and potential side effects.',
        'education': [
            'M.D., University of California, San Francisco',
            'Psychiatry Residency, UCLA Medical Center',
            'B.S. in Biological Sciences, Stanford University'
        ],
        'approaches': [
            'Medication Management',
            'Psychiatric Evaluation',
            'Motivational Interviewing',
            'Brief Cognitive Interventions'
        ],
        'session_cost': '$190',
        'insurance': ['Blue Cross', 'Cigna', 'Aetna', 'Oscar'],
        'languages': ['English', 'Hindi'],
        'video_intro': 'https://example.com/video/michael-patel.mp4'
    },
    {
        'id': 7,
        'name': 'Dr. Sophia Kim',
        'title': 'Child & Adolescent Psychiatrist',
        'photo': 'sophia-kim.jpg',
        'specialty': 'Child & Adolescent Mental Health, ADHD, Anxiety Disorders',
        'experience': '12 years',
        'rating': 4.9,
        'review_count': 115,
        'bio': 'Dr. Kim specializes in psychiatric care for children and adolescents. She works closely with families to create treatment plans that address the unique needs of young people struggling with mental health challenges.',
        'education': [
            'M.D., Yale School of Medicine',
            'Child & Adolescent Psychiatry Fellowship, Children\'s Hospital of Philadelphia',
            'Psychiatry Residency, New York-Presbyterian Hospital',
            'B.A. in Psychology, Columbia University'
        ],
        'approaches': [
            'Medication Management',
            'Family-Centered Care',
            'Collaborative Problem Solving',
            'Behavioral Interventions'
        ],
        'session_cost': '$210',
        'insurance': ['Aetna', 'Blue Cross', 'Cigna', 'UnitedHealthcare', 'Optum'],
        'languages': ['English', 'Korean'],
        'video_intro': 'https://example.com/video/sophia-kim.mp4'
    }
]

counselors = [
    {
        'id': 8,
        'name': 'Jennifer Martinez, LMFT',
        'title': 'Licensed Marriage & Family Therapist',
        'photo': 'jennifer-martinez.jpg',
        'specialty': 'Couples Therapy, Family Relationships, Parenting',
        'experience': '8 years',
        'rating': 4.8,
        'review_count': 89,
        'bio': 'Jennifer specializes in helping couples and families improve communication, resolve conflicts, and strengthen relationships. She creates a supportive environment where all family members can feel heard and valued.',
        'education': [
            'M.S. in Marriage & Family Therapy, Northwestern University',
            'B.A. in Psychology, University of Illinois'
        ],
        'approaches': [
            'Gottman Method Couples Therapy',
            'Emotionally Focused Therapy (EFT)',
            'Structural Family Therapy',
            'Solution-Focused Brief Therapy'
        ],
        'session_cost': '$130',
        'insurance': ['Blue Cross', 'Cigna', 'Aetna'],
        'languages': ['English', 'Spanish'],
        'video_intro': 'https://example.com/video/jennifer-martinez.mp4'
    },
    {
        'id': 9,
        'name': 'David Wilson, LPC',
        'title': 'Licensed Professional Counselor',
        'photo': 'david-wilson.jpg',
        'specialty': 'Grief & Loss, Life Transitions, Men\'s Issues',
        'experience': '11 years',
        'rating': 4.9,
        'review_count': 104,
        'bio': 'David helps clients navigate grief, significant life changes, and personal growth. He has particular expertise in men\'s mental health and creates a space where clients feel comfortable exploring emotions and vulnerability.',
        'education': [
            'M.A. in Counseling Psychology, University of Texas',
            'B.S. in Psychology, Texas A&M University'
        ],
        'approaches': [
            'Existential Therapy',
            'Narrative Therapy',
            'Mindfulness-Based Approaches',
            'Cognitive Behavioral Therapy (CBT)'
        ],
        'session_cost': '$125',
        'insurance': ['Blue Cross', 'Cigna', 'UnitedHealthcare', 'Aetna'],
        'languages': ['English'],
        'video_intro': 'https://example.com/video/david-wilson.mp4'
    },
    {
        'id': 10,
        'name': 'Aisha Johnson, LCSW',
        'title': 'Licensed Clinical Social Worker',
        'photo': 'aisha-johnson.jpg',
        'specialty': 'Trauma Recovery, Racial Identity, Women\'s Issues',
        'experience': '9 years',
        'rating': 4.8,
        'review_count': 92,
        'bio': 'Aisha specializes in trauma-informed therapy with expertise in racial identity development and women\'s issues. She helps clients process past experiences and develop resilience through a culturally responsive approach.',
        'education': [
            'M.S.W., University of Michigan',
            'B.A. in Sociology, Spelman College'
        ],
        'approaches': [
            'Trauma-Focused Cognitive Behavioral Therapy (TF-CBT)',
            'EMDR',
            'Culturally Responsive Therapy',
            'Strengths-Based Approach'
        ],
        'session_cost': '$135',
        'insurance': ['Blue Cross', 'Cigna', 'Aetna', 'UnitedHealthcare'],
        'languages': ['English'],
        'video_intro': 'https://example.com/video/aisha-johnson.mp4'
    },
    {
        'id': 11,
        'name': 'Robert Chen, LMHC',
        'title': 'Licensed Mental Health Counselor',
        'photo': 'robert-chen.jpg',
        'specialty': 'Anxiety, Depression, Stress Management',
        'experience': '7 years',
        'rating': 4.7,
        'review_count': 78,
        'bio': 'Robert helps clients manage anxiety, depression, and stress through practical coping strategies and personal insight. He believes that therapy should be accessible and relevant to daily life.',
        'education': [
            'M.A. in Mental Health Counseling, Boston University',
            'B.A. in Psychology, Tufts University'
        ],
        'approaches': [
            'Cognitive Behavioral Therapy (CBT)',
            'Acceptance and Commitment Therapy (ACT)',
            'Mindfulness-Based Stress Reduction',
            'Solution-Focused Brief Therapy'
        ],
        'session_cost': '$120',
        'insurance': ['Blue Cross', 'Cigna', 'Optum', 'Aetna'],
        'languages': ['English', 'Mandarin Chinese'],
        'video_intro': 'https://example.com/video/robert-chen.mp4'
    }
]

# Combine all professionals
all_professionals = psychologists + psychiatrists + counselors

# Helper function to generate sample availability
def generate_availability():
    availability = {}
    start_date = datetime.now()
    
    # Generate 14 days of availability
    for i in range(14):
        day = start_date + timedelta(days=i)
        day_str = day.strftime('%Y-%m-%d')
        
        # No availability on weekends
        if day.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            availability[day_str] = []
            continue
            
        # Generate time slots for this day
        time_slots = []
        start_hour = 9  # 9 AM
        
        while start_hour < 17:  # Until 5 PM
            # Randomly skip some hours to create realistic availability
            if random.random() < 0.3:  # 30% chance to skip this hour
                start_hour += 1
                continue
                
            for minutes in [0, 30]:  # 30-minute slots
                slot_time = f"{start_hour:02d}:{minutes:02d}"
                time_slots.append(slot_time)
                
            start_hour += 1
            
        availability[day_str] = time_slots
        
    return availability


@professional_bp.route('/professional-help')
def professionals_home():
    featured_professionals = random.sample(all_professionals, min(3, len(all_professionals)))
    return render_template('professionals/professionals_home.html', 
                          featured_professionals=featured_professionals)


@professional_bp.route('/professional-help/psychologists')
def psychologists_page():
    for psychologist in psychologists:
        psychologist['image_url'] = url_for('static', filename='images/emma-bennett.jpg')
    return render_template('professionals/psychologists.html', psychologists_professionals=psychologists)

@professional_bp.route('/professional-help/psychiatrists')
def psychiatrists_page():
    for psychiatrist in psychiatrists:
        psychiatrist['image_url'] = url_for('static', filename='images/emma-bennett.jpg')
    return render_template('professionals/psychiatrists.html', psychiatrists_professionals=psychiatrists)


@professional_bp.route('/professional-help/counselors')
def counselors_page():
    for counselor in counselors:
        counselor['image_url'] = url_for('static', filename='images/emma-bennett.jpg')
    return render_template('professionals/counselors.html', counselors_professionals=counselors)


@professional_bp.route('/professional-help/professional/<int:professional_id>')
def professional_detail(professional_id):
    professional = next((p for p in all_professionals if p['id'] == professional_id), None)
    
    if not professional:
        flash('Professional not found', 'error')
        return redirect(url_for('professional_bp.professionals_home'))
        
    # Get reviews for this professional (sample data)
    reviews = generate_reviews(professional)
    
    return render_template('professionals/professional_detail.html', 
                          professional=professional,
                          reviews=reviews)


@professional_bp.route('/professional-help/booking/<int:professional_id>')
def booking(professional_id):
    if not session.get('user_id'):
        flash('Please log in to book a session', 'error')
        return redirect(url_for('user_bp.login'))
        
    professional = next((p for p in all_professionals if p['id'] == professional_id), None)
    
    if not professional:
        flash('Professional not found', 'error')
        return redirect(url_for('professional_bp.professionals_home'))
        
    # Generate availability for this professional
    availability = generate_availability()
    
    return render_template('professionals/booking.html', 
                          professional=professional,
                          availability=availability)


@professional_bp.route('/api/professional/availability/<int:professional_id>', methods=['GET'])
def get_availability(professional_id):
    professional = next((p for p in all_professionals if p['id'] == professional_id), None)
    
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404
        
    # Generate availability for this professional
    availability = generate_availability()
    
    return jsonify(availability)


@professional_bp.route('/api/professional/book-session', methods=['POST'])
def book_session():
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'Please log in to book a session'}), 401
        
    data = request.json
    professional_id = data.get('professional_id')
    date = data.get('date')
    time = data.get('time')
    session_type = data.get('session_type')
    notes = data.get('notes', '')
    
    if not all([professional_id, date, time, session_type]):
        return jsonify({'success': False, 'message': 'Missing required booking information'}), 400
        
    professional = next((p for p in all_professionals if p['id'] == int(professional_id)), None)
    if not professional:
        return jsonify({'success': False, 'message': 'Professional not found'}), 404
    
    # In a real app, would save the booking to the database
    # Here we just return success with confirmation details
    booking_data = {
        'id': random.randint(10000, 99999),
        'professional': professional['name'],
        'date': date,
        'time': time,
        'session_type': session_type,
        'confirmation_code': f"BK{random.randint(100000, 999999)}"
    }
    
    return jsonify({
        'success': True, 
        'message': 'Session booked successfully',
        'booking': booking_data
    })


# Helper function to generate sample reviews
def generate_reviews(professional):
    review_count = professional['review_count']
    # Generate a subset of reviews (up to 5)
    sample_count = min(5, review_count)
    
    reviewer_names = [
        'Michael S.', 'Jennifer L.', 'David W.', 'Sarah T.', 
        'Robert J.', 'Emily C.', 'Daniel M.', 'Olivia P.',
        'James R.', 'Sophia K.', 'Thomas H.', 'Emma B.'
    ]
    
    review_texts = [
        f"Dr. {professional['name'].split()[1]} has been incredibly helpful in my journey toward better mental health. Their approach is both professional and compassionate.",
        f"I've been seeing {professional['name'].split()[0]} for a few months now, and I've made more progress than I did in years of previous therapy.",
        f"Very knowledgeable and attentive. {professional['name'].split()[0]} really listens and offers practical strategies that have made a big difference in my life.",
        f"The sessions with {professional['name'].split()[0]} have given me tools to manage my anxiety that I use every day. Highly recommended!",
        f"{professional['name']} creates such a safe and supportive environment. I never feel judged and can be completely honest during our sessions.",
        f"I was hesitant to try therapy, but {professional['name'].split()[0]} has made the experience so positive. Their expertise is evident in every session.",
        f"Working with {professional['name']} has been transformative. They have helped me understand myself better and develop healthier coping mechanisms.",
        f"I appreciate how {professional['name'].split()[0]} combines evidence-based techniques with genuine empathy. They're truly invested in their clients' wellbeing.",
        f"{professional['name'].split()[0]} is an exceptional therapist. They challenge me when needed but always with kindness and support.",
        f"The progress I've made with {professional['name']} has been noticed by friends and family. I'm so grateful for their guidance."
    ]
    
    reviews = []
    for i in range(sample_count):
        rating = round(max(3.5, min(5, professional['rating'] + random.uniform(-0.5, 0.5))), 1)
        date = datetime.now() - timedelta(days=random.randint(1, 120))
        
        review = {
            'id': i + 1,
            'author': random.choice(reviewer_names),
            'rating': rating,
            'date': date.strftime('%B %d, %Y'),
            'content': random.choice(review_texts),
            'helpful_count': random.randint(0, 15)
        }
        reviews.append(review)
    
    return reviews