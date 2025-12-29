@login_required
def state_head_reports_builder(request):
    """State Head Report Builder - Excludes financial columns"""
    # Check if user is a state admin
    if not request.user.is_superuser:
        try:
            user_state = request.user.state_profile
            if not user_state.approved:
                messages.error(request, 'Access denied.')
                return redirect('index')
        except UserState.DoesNotExist:
            messages.error(request, 'Access denied. Only state heads can access this report builder.')
            return redirect('index')
    
    user_state = None
    if not request.user.is_superuser:
        try:
            user_state = request.user.state_profile.state
        except:
            pass
    
    # Define columns available to state heads (excluding financial data)
    veteran_columns = [
        {'name': 'association_id', 'label': 'Association ID', 'type': 'text'},
        {'name': 'association_number', 'label': 'Association Number', 'type': 'text'},
        {'name': 'name', 'label': 'Name', 'type': 'text'},
        {'name': 'service_number', 'label': 'Service Number', 'type': 'text'},
        {'name': 'rank', 'label': 'Rank', 'type': 'text'},
        {'name': 'branch', 'label': 'Branch', 'type': 'text'},
        {'name': 'state', 'label': 'State', 'type': 'text'},
        {'name': 'date_of_birth', 'label': 'Date of Birth', 'type': 'date'},
        {'name': 'contact', 'label': 'Contact', 'type': 'text'},
        {'name': 'address', 'label': 'Address', 'type': 'text'},
        {'name': 'living_city', 'label': 'Living City', 'type': 'text'},
        {'name': 'zip_code', 'label': 'ZIP Code', 'type': 'text'},
        {'name': 'alternate_email', 'label': 'Alternate Email', 'type': 'text'},
        {'name': 'blood_group', 'label': 'Blood Group', 'type': 'text'},
        {'name': 'medical_category', 'label': 'Medical Category', 'type': 'text'},
        {'name': 'nearest_echs', 'label': 'Nearest ECHS', 'type': 'text'},
        {'name': 'nearest_dhq', 'label': 'Nearest DHQ', 'type': 'text'},
        {'name': 'educational_qualification', 'label': 'Educational Qualification', 'type': 'text'},
        {'name': 'emergency_contact_name', 'label': 'Emergency Contact Name', 'type': 'text'},
        {'name': 'emergency_contact_phone', 'label': 'Emergency Contact Phone', 'type': 'text'},
        {'name': 'date_of_joining', 'label': 'Date of Joining', 'type': 'date'},
        {'name': 'retired_on', 'label': 'Retired On', 'type': 'date'},
        {'name': 'unit_served', 'label': 'Last Ship Served', 'type': 'text'},
        {'name': 'specialization', 'label': 'Specialization', 'type': 'text'},
        {'name': 'decorations', 'label': 'Awards & Decorations', 'type': 'text'},
        {'name': 'enrolled_date', 'label': 'Enrolled Date', 'type': 'date'},
        {'name': 'association_date', 'label': 'Association Date', 'type': 'date'},
        {'name': 'membership', 'label': 'Membership Status', 'type': 'boolean'},
        {'name': 'subscription_paid_on', 'label': 'Subscription Paid On', 'type': 'date'},
        {'name': 'spouse_name', 'label': 'Spouse Name', 'type': 'text'},
        {'name': 'spouse_contact', 'label': 'Spouse Contact', 'type': 'text'},
        {'name': 'children_count', 'label': 'Children Count', 'type': 'text'},
        {'name': 'next_of_kin', 'label': 'Next of Kin', 'type': 'text'},
        {'name': 'next_of_kin_relation', 'label': 'Next of Kin Relation', 'type': 'text'},
        {'name': 'next_of_kin_contact', 'label': 'Next of Kin Contact', 'type': 'text'},
        {'name': 'approved', 'label': 'Approval Status', 'type': 'boolean'},
        {'name': 'created_at', 'label': 'Created At', 'type': 'date'},
        {'name': 'updated_at', 'label': 'Updated At', 'type': 'date'},
    ]
    
    # Only show current state for state heads
    states = []
    if request.user.is_superuser:
        states = State.objects.all().order_by('name')
    elif user_state:
        states = [user_state]
    
    saved_configs = ReportConfiguration.objects.filter(
        django_models.Q(created_by=request.user) | django_models.Q(is_template=True),
        report_type='veteran'
    )
    
    return render(request, 'veteran_app/state_head_reports_builder.html', {
        'veteran_columns': veteran_columns,
        'states': states,
        'saved_configs': saved_configs,
        'user_state': user_state
    })

@login_required
def generate_state_head_report(request):
    """Generate and download state head report (no financial data)"""
    if request.method != 'POST':
        return redirect('state_head_reports_builder')
    
    import csv
    from datetime import datetime
    
    selected_columns = request.POST.getlist('columns')
    if not selected_columns:
        messages.error(request, 'Please select at least one column.')
        return redirect('state_head_reports_builder')
    
    # Validate that no financial columns are selected
    financial_columns = ['bank_account', 'bank_name', 'pension_details', 'welfare_schemes']
    if any(col in financial_columns for col in selected_columns):
        messages.error(request, 'Financial columns are not available in state head reports.')
        return redirect('state_head_reports_builder')
    
    state_filter = request.POST.get('state_filter')
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    date_field = request.POST.get('date_field')
    membership_filter = request.POST.get('membership_filter')
    approval_filter = request.POST.get('approval_filter')
    export_format = request.POST.get('export_format', 'csv')
    
    # Validate dates
    today = datetime.now().date()
    if from_date:
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
        if from_date_obj > today:
            messages.error(request, 'From Date cannot be a future date.')
            return redirect('state_head_reports_builder')
    if to_date:
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
        if to_date_obj > today:
            messages.error(request, 'To Date cannot be a future date.')
            return redirect('state_head_reports_builder')
    if from_date and to_date and from_date > to_date:
        messages.error(request, 'From Date cannot be later than To Date.')
        return redirect('state_head_reports_builder')
    
    queryset = VeteranMember.objects.all()
    
    # State head access control
    if not request.user.is_superuser:
        try:
            user_state = request.user.state_profile.state
            queryset = queryset.filter(state=user_state)
        except:
            messages.error(request, 'Access denied.')
            return redirect('index')
    elif state_filter:
        queryset = queryset.filter(state_id=state_filter)
    
    # Apply filters
    if from_date and to_date and date_field:
        filter_kwargs = {f"{date_field}__range": [from_date, to_date]}
        queryset = queryset.filter(**filter_kwargs)
    
    if membership_filter:
        queryset = queryset.filter(membership=(membership_filter == 'true'))
    
    if approval_filter:
        queryset = queryset.filter(approved=(approval_filter == 'true'))
    
    queryset = queryset.select_related('state', 'rank', 'branch', 'blood_group')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=\"state_head_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv\"'
    
    writer = csv.writer(response)
    headers = [col.replace('_', ' ').title() for col in selected_columns]
    writer.writerow(headers)
    
    for member in queryset:
        row = []
        for col in selected_columns:
            if col == 'state':
                row.append(member.state.name)
            elif col == 'rank':
                row.append(member.rank.name)
            elif col == 'branch':
                row.append(member.branch.name)
            elif col == 'blood_group':
                row.append(member.blood_group.name)
            elif col == 'medical_category':
                row.append(member.medical_category.name if member.medical_category else member.medical_category_text or '')
            elif col == 'nearest_echs':
                row.append(member.nearest_echs.name if member.nearest_echs else member.nearest_echs_text or '')
            elif col == 'nearest_dhq':
                row.append(member.nearest_dhq_text or '')
            elif col == 'membership':
                row.append('Active' if member.membership else 'Inactive')
            elif col == 'approved':
                row.append('Approved' if member.approved else 'Pending')
            else:
                value = getattr(member, col, '')
                row.append(value if value else '')
        writer.writerow(row)
    
    return response