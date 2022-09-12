# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


INDIRECT_QUESTIONS = [
    '<p>Has E&S been incorporated into the FI’s vision, mission and values including formal commitments relating to E&S?</p>',
    '<p>Have material E&S considerations been integrated into the FI’s business strategy?</p>',
    '<p>Has the board clearly articulated the importance of E&S for the success of the FI and communicated this throughout the organisation?</p>',
    '<p>Does the FI have E&S related policies in place (e.g. environmental, financial inclusion, human rights, whistleblowing and AML/CFT policies or stand alone E&S policy)?</p><p> Do these policies comply with applicable international / national E&S standards, regulations and sectoral guidelines or industry initiatives?</p>',
    '<p>Does the FI adhere to an E&S exclusion list, which is in alignment with the AGF’s Exclusion List or the IFC’s Exclusion List?</p>',
    '<p>Is the FI a member of or signatory to any industry associations or bodies that promote responsible E&S management practices?</p>',
    '<p>Has the FI adopted and implemented an E&S Management System that:</p><ul><li>encompasses all of company activities?</li><li>is commensurate to the level of E&S risk exposure?</li><li>- includes E&S risk screening, categorisation, due diligence and investment/transaction monitoring procedures?</li><li>comprises of documented management programmes and plans to systematically ensure the effective implementation of the ESMS?</li></ul>',
    '<p>Does the FI have an internal audit function responsible for assessing levels of compliance with its E&S policies and procedures?</p>',
    '<p>Does the FI have a process to categorise E&S risks for credit opportunities? </p>',
    '<p>Does the FI have client due diligence procedures in place that incorporates E&S considerations (e.g.  identify potential material E&S risks and E&S-related opportunities) into these investment activities?</p>',
    '<p>Does the FI have a process in place which enables the integration of E&S risk review at the level of the Credit Committee?</p>',
    '<p>Does the FI require its clients to report on their E&S performance, including E&S incidents; data and progress towards completion of any corrective action plans post-investment / post-transaction?</p>',
    '<p>Does the FI conduct periodic site visits to monitor its clients’ E&S performance?</p>',
    '<p>Does the FI disclose any E&S related information, either internally and / or externally, including material E&S incidents?</p>',
    '<p>Has the FI assigned responsibility to personnel(s) for implementing the E&S management system and for identifying and mitigating E&S risks and impacts? This should include formally designating responsibility to the Board of Directors, a Board Sub-Committee (e.g. the Risk and Compliance Committee), and Management Executives)</p><p>Does the FI make use of external resources to support its E&S management efforts?</p>',
    '<p>Does the FI provide appropriate training, assistance and or / external resources for employees to help them understand and identify the relevant and importance of E&S factors in investment activities and enhance their knowledge around the FI’s E&S management system?</p>',
    '<p>Is the FI engaged in financing any of the activities, or companies engaged in such activities, included in the AGF’s Exclusion List or the IFC’s Exclusion List? Which sectors and the proportion of the total portfolio involved in such activities.</p>',
    '<p>Has any of the FI’s customers or the FI received any significant fines, penalties, claims or notices associated with the E&S aspects of its activities in the past 5 years?</p>',
    '<p>Has the FI or any of the FI’s customers been the subject of negative attention from the media or NGOs? This information should be supplemented by conducting an external factors review using key words related to the company and relevant E&S topics in a web based search engine.</p>',
    '<p>Does the FI assist and support its clients in driving E&S performance and the management of E&S-related risks and opportunities? Including:</p><ul><li>reviewing clients existing compliance?</li><li>implementing monitoring and reporting processes to assess portfolio companies’ management of E&S factors?</li><li>initiating and / or supporting portfolio company on specific E&S initiatives e.g. major incident, risk management practices/efforts?</li><li>engaging and interacting with the board on E&S issues?</li><li>systematically following-up on E&S incidents / accidents reported?</li></ul>'
]

INDIRECT_QUESTIONS_CRITERIA = [
    'Management Commitment',
    'Management Commitment',
    'Management Commitment',
    'Management System - Policy',
    'Management System - Policy',
    'Management System - Policy',
    'Management System - Procedures',
    'Management System - Procedures',
    'Management System - Credit E&S risk Review',
    'Management System - Credit E&S risk Review',
    'Management System - Credit E&S risk Review',
    'Management System - Monitoring and Reporting',
    'Management System - Monitoring and Reporting',
    'Management System - Monitoring and Reporting',
    'Capacity and Competency',
    'Capacity and Competency',
    'Reputational Risk Review',
    'Reputational Risk Review',
    'Reputational Risk Review',
    'Value Add',
]

INDIRECT_QUESTIONS_STANDARD = [
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS2',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
]

INDIRECT_QUESTIONS_WTA = [
    '[E&S statement or policy; E&S/ reports (integrated / standalone); company website]',
    '[Documentation outlining the integration of E&S considerations into business processes - the objective here is to have a E&S MS that is not stand-alone or implemented in silo from other business and credit risk management systems]',
    '[Board meeting minutes; board of director communication; E&S reports (integrated / standalone); discussion with board members and management]',
    '[Documented E&S related policies; discussions with management]',
    '[Own documented exclusion list; IFC exclusion list]',
    '[Memberships inventory / list; membership certificates; discussion with management]',
    '[ESMS Manual; documentation on ESMS procedures, supporting tools and templates such as questionnaire, registers, forms, etc.]',
    '[Internal audit procedural documentation]',
    '[E&S risk review and categorisation procedure, supporting tools, etc.]',
    '[Due diligence procedural documentation; due diligence reports/ records/outputs; discussions with management, etc.]',
    '[E&S information note to the Credit Committee; deal structuring procedural document; example E&S clauses / provisions; example deal agreements; Environmental & Social Action Plans]',
    '[Monitoring and reporting mechanisms and processes; monitoring data / records; example action plans; incident report; discussions with management]',
    '[Monitoring and reporting processes]',
    '[Bi-annual, annual or quarterly reports; communication channels (e.g. emails); major incident reporting; board agenda and meeting minutes; committee meeting minutes; company newsletters; discussions with management] ',
    '[List of person(s) involved with E&S and describe of roles; person(s) position within the organisation; qualification / experience / CVs; external service provider name and scope of work; discussions with management]',
    '[Training materials; training attendance registers / log; training programme / schedule; description of training; training certificates; name of service provider (if any); discussions with management]',
    '[Google search using key words; IFC Exclusion List; investment portfolio; investment mandate; discussions with management]',
    '[Google search using key words; Legal DD; internal / external audits; fines/claims; SME\'s response to fines, penalties, litigations on E&S matters; discussions with management]',
    '[Google search using key words; SME\'s response to adverse media campaign; discussions with management]',
    '[Monitoring processes in place to assess portfolio companies’ management of E&S factors; monitoring and reporting structures; communication with portfolio companies; meeting minutes; email correspondence; E&S budget allocation; E&S reports; discussions with management]',
]

INDIRECT_QUESTIONS_GAPS = [
    '[E&S Policy inexistent, E&S Policy confusing with CSR (not risk-oriented) or not referring to international standards, no sustainable report, no E&S information on web-site, etc.]',
    '[E&S Policy and systems are stand-alone (separate tools) and not included in the credit cycle system.]',
    '[Board meeting minutes do not include E&S, no integrated or stand-alone E&S report, etc.]',
    '[Short and clearly worded. Articulates the E&S objectives and principles that guide the FI to achieve sound E&S performance. Specifies compliance with the local and international applicable laws and regulations and, where appropriate, with international standards (e.g. IFC Performance Standards,  IFC Interpretation Note on FIs, AfDB Safeguards).]',
    '[No documented E&S exclusion list, no documented evidence (checklist or other tools) demonstrating clear use of an exclusion list as part of the screening phase, etc. Interviews with credit officers showing lack of knowledge of the exclusion list - note that existence of clients in the FI portfolio with activities that may trigger the exclusion list is discussed in Question 18.]',
    '[Equator Principles, UN PRI, UN Global Compact, local sustainability standard (Sustainable Finance Initiative in Kenya, Sustainable Banking Principles in Nigeria, etc.]',
    '[An insufficient ESMS (i) does not reflects the key issues – both risks and opportunities – that the FI needs to manage, (ii) has a scope that is restrited (for example to one credit line only), (iii) has procedures but no supporting tools, (iv) is generic and not tailored to the FI organisation, departments and types of products, (v) is outdated and has never been reviewed, etc.',
    '[Internal audit does not include E&S, no audit report; no E&S internal audit checklist assessing the procedures developed as part of the FI\'s ESMS. Senior mangement not involed into the periodic performance reviews of the effectiveness of the ESMS.]',
    '[No documented evidence of E&S risk review procedure integrating factors such as type of product, type of activity, duration; E&S risk categorisation (e.g. low, medium, high) that is inconsistent with the levels of approval, etc.]',
    '[No documented Environmental & Social Due Diligence questionnaire, no process for external Environmental & Social Due Diligence for high risks, no examples of Due Diligence reports, no examples of Environmental & Social Action Plan, etc.][Customer diligence procedures do not include media searches, interviews with employees, documentation review and questionnaires., etc.]',
    '[Credit Committee information note does not include E&S risk review summary, no documented evidence of the integration of E&S covenants into investment agreements (e.g. no mention of compliance with applicable standards and guidelines, no examples of corrective actions identified as part of the due diligence process), etc.]',
    '[No identification of E&S Key Performance Indicators; no evidence of annual monitoring report; no updated Environmental and Social Action Plans, no evidence of incident report, etc.]',
    '[No evidence of documented site visit reports; site visit reports do not include E&S aspects; no documented subsequent actions following site visits, etc.]',
    '[FI’s annual or quarterly reports do not include E&S related information; no examples of major incident reports, etc.]',
    '[Individuals do not have the mandate and authority to implement the ESMS; no evidence of a senior management individual (e.g. Board member) supporting the overarching implementation of the ESMS goals and objectives; no evidence of a full-time mid-level individual (e.g. E&S Officer / Manager) ensuring day-to-day E&S integration, etc.]',
    '[No training conducted; training relating to CSR instead of E&S issues and risks relating to the FI\'s portfolio; interviews with credit officers revealing little to no knowledge of the implementation of E&S into the credit process, etc.] Assess whether the FI would require Capacity Development Assistance as a mitigation measure.]',
    '[Inconsistencies, or no alignment with the sectors listed by the FI and actual activities financed / invested into.]',
    '[Evidence of significant fines, penalties, claims, notices; no evidence of adequate subsequent steps / actions undertaken, etc.]',
    '[Evidence of negative attention from reliable sources; no evidence of subsequent steps / actions undertaken, etc.]',
    '[No evidence of communication with portfolio companies; minutes of meetings, E&S reports, etc.]',
]

DIRECT_QUESTIONS = [
    '<p>Describe the SME’s activities. </p>',
    '<p>Provide a list of the SME’s site(s).</p>',
    '<p>Provide a description of the SME’s staff/personnel.</p>',
    '<p>Describe the SME’s employment conditions, including types of contracts, working hours, salaries relating to legal minimum wages and social benefits.</p><p>Provide any gender related information (e.g. gender distribution, share of women in management positions).</p>',
    '<p>Describe the main energy sources utilised by the SME and its activities.</p>',
    '<p>Provide a list of the main raw materials utilised by the SME.</p>',
    '<p>Provide a list of the main suppliers to the SME.</p>',
    '<p>Are the SME’s activities located alongside or nearby sensitive areas from an environmental perspective?</p>',
    '<p>Are the SME’s activities located alongside or nearby sensitive areas from a social perspective?</p>',
    '<p>Has the SME adopted and implemented policies, certifications, procedures, trainings, hired dedicated resources, etc. relating to the management of environment, health & safety at work, employment and social welfare?</p>',
    '<p>Are emergency response plans in place within the SME?</p>',
    '<p>Has the SME established a grievance mechanism/management system (internal and external)?</p>',
    '<p>Does the SME provide its employees with adequate employment terms and salaries?</p>',
    '<p>Has the SME experienced or recorded grievances/litigation cases or strikes related to employment in the last 3 years?</p>',
    '<p>Has the SME experienced or recorded accidents, occupational illnesses or any other complaints/litigation cases relating to Occupational Health & Safety in the last 3 years?</p>',
    '<p>Does the SME provide its employees with a safe work environment?</p>',
    '<p>Does the SME’s have the required environmental permits for carrying out its activities?</p>',
    '<p>Has the SME experienced environmental accidents and/or environmental litigation in the last 3 years?</p>',
    '<p>Does the SME generate significant pollution?</p>',
    '<p>Has the SME experienced or recorded grievances/litigation arising from communities, NGOs, etc. in the course of the last 3 years?</p>',
    '<p>Has the SME implemented community development initiatives?</p>',
    '<p>Has the SME taken steps to ensure that security measures do not pose a risk for the communities or for the employees?</p>',
    '<p>Is the SME involved in activities, included in the AGF’s Exclusion List or the IFC’s Exclusion List? Which sectors and the proportion of the operations involved in such activities.</p>',
    '<p>Has the SME received any significant fines, penalties, claims or notices associated with the E&S aspects of its activities in the past 5 years (publicly available information)?</p>',
    '<p>Has the SME been the subject of negative attention from the media or NGOs? This information should be supplemented by conducting an external factors review using key words related to the company and relevant E&S topics in a web based search engine.</p>',
]


DIRECT_QUESTIONS_CRITERIA = [
    'General',
    'General',
    'General',
    'General',
    'General',
    'General',
    'General',
    'General',
    'General',
    'Management System ',
    'Management System ',
    'Management System ',
    'Labour Conditions, Occupational Health & Safety ',
    'Labour Conditions, Occupational Health & Safety ',
    'Labour Conditions, Occupational Health & Safety ',
    'Labour Conditions, Occupational Health & Safety ',
    'Pollution Prevention and Control',
    'Pollution Prevention and Control',
    'Pollution Prevention and Control',
    'Community Health & Safety ',
    'Community Health & Safety ',
    'Community Health & Safety ',
    'Reputational Risk Review ',
    'Reputational Risk Review ',
    'Reputational Risk Review ',
    'Other'
]

DIRECT_QUESTIONS_STANDARD = [
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS2 AfDB OS5',
    'IFC PS2 AfDB OS5',
    'IFC PS2 AfDB OS5',
    'IFC PS2 AfDB OS5',
    'IFC PS3 AfDB OS4',
    'IFC PS3 AfDB OS4',
    'IFC PS3 AfDB OS4',
    'IFC PS4 AfDB OS1',
    'IFC PS4 AfDB OS1',
    'IFC PS4 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
    'IFC PS1 AfDB OS1',
]

DIRECT_QUESTIONS_WTA = [
    '[Sector, clients, production information, revenue, history, etc.]',
    '[Location or address, area of the buildings and the land, type of lease or title deed, etc.]',
    '[Number of employees (permanent/temporary detail), seasonal variations, etc.]',
    '[Existence of documented contracts or not;Number of weekly work hours (overtime and time off details);Monthly (or daily) salaries with social benefits and welfare;Gender distribution,  share of women in management positions]',
    '[Electricity, diesel, etc.]',
    '[Cotton, ores, paper, etc.]',
    '[Small scale planters, textile wholesalers, etc.]',
    '[Location and distance of water points (rivers, lakes, wells etc.) nearest to the site and all other sites of environmental importance (protected areas, national parks, etc.)]',
    '[Location and distance of neighbouring communities, residential areas, buildings open to the public (schools, hospitals, hotels, etc.) that can be affected by the activities of your SME.]',
    '[Environmental Policy, Health and Safety Policy, HR Policy, CSR Policy, including clauses around the prevention of child labour and forced labour, etc.) certifications, procedures and manual (waste management, employee manual, etc.), health and safety committee, EHS or HR manager, trainings (first aid, fire, etc.)]',
    '[Fire evacuation plan, casualty treatment plan, crisis management plan, etc.]',
    '[Any formal or information system to collect and record the complaints that employees, communities, clients, suppliers can have and systems to address such complaints in a prompt and efficient manner.]',
    '[Formal written contract of employment]',
    '[Provide details of employees complaints or grievances in the context of employment termination for example, formal notice and labour inspectorate fine, etc.]',
    '[Lost time accidents, fatal accidents, occupational illnesses, etc. are examples of accidents to report. Discuss any lawsuit with an employee following an accident or an illness, formal notice or labour inspectorate fine regarding occupational health and safety, etc.]',
    '[Personal Protective Equipment such as safety boots, gloves, hard hats, respiratory masks, reflective vests); fire safety equipment, alarms and fire detection; ventilation of premises; marchine guarding safety, etc.]',
    '[Permits and environmental impact assessments, authorisation or declaration from NEMA, permits to operate groundwater boreholes, permit to discharge wastewater, etc.]',
    '[Fires, discharge of chemical products into the ground or river, waste disposal, etc. are examples of environmental accidents. Provide details relating to complaints about the noise, letters of formal notice or fines from the environmental authorities, etc.]',
    '[Wasterwater, hazardous wastes, etc.]',
    '[Provide details relating to land disputes, community grievances relating to pollution, safety, etc.]',
    '[Community development initiatives (CSR process, external grievances management, external relations/community liaison officer, etc.) may include donations, priority in hiring, trainings, regular meetings to discuss different grievances, water supply, etc. ]',
    '[Security personnel may pose a risk to local communities or employees in cases of non-ehtical behaviour, threats, use of arms, etc.]',
    '[Google search using key words; details relating to the activities of the SME (e.g workforce), etc.]',
    '[Google search using key words; public litigations; internal /external audits; fines / claims;  SME\'s response to fines, penalties, litigations on E&S matters;  discussions with management, etc.]',
    '[Community development initiatives (CSR process, external grievances management, external relations/community liaison officer, etc.) may include donations, priority in hiring, trainings, regular meetings to discuss different grievances, water supply, etc. ]',
]

DIRECT_QUESTIONS_GAPS = [
    'N/A',
    'N/A',
    'N/A',
    'N/A',
    'N/A',
    'N/A',
    'N/A',
    '[No protection perimeter from water points (well, river, etc.), environmentally sensitive areas nearby (e.g. protected areas, national parks, etc.)]',
    '[Neighbouring communities, residential areas, buildings open to the public (schools, hospitals, hotels, etc.) close by that can be affected by the operations of the SME.]',
    '[No docoumented policies relating to Environment, Health and Safety, HR, including clauses around the prevention of child labour and forced labour, etc.), no documented evidence of E&S procedures (waste management, employee manual, etc.), no evidence of health and safety committee, no EHS or HR manager, no evidence of training registers (first aid, fire, etc.)]',
    '[No documented evidence of fire evacuation plan, no evidence of fire safety  equipment, etc.]',
    '[No documented evidence of grievance registers (internal and external), etc.]',
    '[Verbal agreements, contract of employment missing key information such as salaries, working hours, overtime, etc.]',
    '[No evidence of documented grievance register, litigation register, etc.]',
    '[No documented evidence of records / registers relating to occupational accidents; formal notice or labour inspectorate fine relating to occupational health and safety, labour, etc.]',
    '[No documented evidence of Health & Safety Committee minutes, etc.]',
    '[No EIA; no evidence of relevant permits, authorisation or declaration from competent authorities; no documented evidence of environmental management plan in line with EIA, etc.]',
    '[No documented E&S incident register, documented incident register with no associated corrective actions, etc.]',
    '[No documented dashboard, including amount, type of waste generated, disposal means, no documented wastecarrier accredidation for hazardous waste, etc.]',
    '[No documented external grievance register and associated mitigation measures; documented register with no evidence of associated mitigations measures, etc.]',
    '[No evidence of documented CSR initiative process, external grievances management, minutes of meetings, communication channels with communities, etc.]',
    '[No documented Code of Conduct for security personnel relating to ethical behaviour, harassment, threats, use of arms, etc.]',
    '[Evidence of illegal activities, child labour, etc.]',
    '[Evidence of significant fines, penalties; no documented evidence of subsequent corrective actions undertaken, etc.]',
    '[Evidence of negative attention from reliable sources; no documented subsequent steps / actions undertaken, etc.]',
]


class agfInternalDDQuestionnaire(models.Model):
    _inherit = 'agf.questionnaire'

    questionnaire_type = fields.Selection([('NA','NA'),('Direct','Direct'),('Indirect','Indirect')], default='NA', string='Questionnaire Type')
    category = fields.Char(related='category_fi_sme_id.name')
    institution_type = fields.Selection(
        [('Financial Institution', 'Financial Institution'), ('Corporate', 'Corporate'), ('SME', 'SME')], related='screening_id.types_of_institution', readonly=True)
    category_fi_sme_id = fields.Many2one('agf.fi.category', domain="[('category_type', '=', institution_type)]")
    action_plan_extra_ids = fields.One2many('agf.template.actionplan.extra', 'questionnaire_id', ondelete='cascade')
    action_plan_ids = fields.One2many('agf.template.actionplan', 'questionnaire_id', ondelete='cascade')
    questions_ids = fields.One2many('agf.template.questions', 'questionnaire_id', ondelete='cascade')


    @api.onchange('questionnaire_type')
    def _onchange_questionnaire_type(self):
        values = []
        QUESTIONS = []
        CRITERIAS = []
        for rec in self:
            for entry in rec.questions_ids:
                entry.unlink()
            if rec.questionnaire_type:
                if rec.questionnaire_type == 'Indirect':
                    QUESTIONS = INDIRECT_QUESTIONS
                    CRITERIAS = INDIRECT_QUESTIONS_CRITERIA
                    STANDARDS = INDIRECT_QUESTIONS_STANDARD
                    WTA = INDIRECT_QUESTIONS_WTA
                    GAPS = INDIRECT_QUESTIONS_GAPS
                if rec.questionnaire_type == 'Direct':
                    QUESTIONS = DIRECT_QUESTIONS
                    CRITERIAS = DIRECT_QUESTIONS_CRITERIA
                    STANDARDS = DIRECT_QUESTIONS_STANDARD
                    WTA = DIRECT_QUESTIONS_WTA
                    GAPS = DIRECT_QUESTIONS_GAPS
                i = 0
                j = 0
                for criteria in CRITERIAS:
                    i += 1
                    if i == 26:
                        r_question = {
                            'name': i,
                            'assessment_criteria': criteria,
                            'standards': '',
                            'question': '',
                            'wta': '',
                            'findings_yes_no': 'NA',
                            'gaps': '',
                        }
                    else:
                        r_question = {
                            'name': i,
                            'assessment_criteria': criteria,
                            'standards': STANDARDS[j],
                            'question': QUESTIONS[j],
                            'wta': WTA[j],
                            'findings_yes_no': 'NA',
                            'gaps': GAPS[j],
                        }
                    j += 1
                    if rec.questions_ids:
                        values.append((6, 0, r_question))
                    else:
                        values.append((0, 0, r_question))
                self.questions_ids = values


class FICategory(models.Model):
    _name = 'agf.fi.category'
    _description = 'Category for Financial Institution, Corporate and SME'

    name = fields.Char('Category name')
    category_type = fields.Selection([('Financial Institution','Financial Institution'),('Corporate','Corporate'),('SME','SME')], string='Category Type')