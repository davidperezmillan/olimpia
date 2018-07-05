from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Series, TorrentServers, Plugins,TelegramChatIds



CHOICES = (( False,'No',), ( True,'Si',))
CHOICES_QUALITY = (( 'NR','NR',),( 'HD','HD',),( 'VO','VO',),( 'AL','AL',), )

class SeriesForm(forms.ModelForm):
    
    ep_start = forms.CharField(max_length=8, min_length=8,  initial="NRS00E00",widget=forms.TextInput(attrs={'readonly':'readonly'}))
    ep_end = forms.CharField(max_length=8, min_length=8,  initial="NRS99E99",widget=forms.TextInput(attrs={'readonly':'readonly'}))
    quality = forms.CharField(max_length=2, min_length=2,  initial="NR",widget=forms.Select(attrs={},choices=CHOICES_QUALITY))
    
    
    class Meta:
        model = Series
        fields = ('author', 'nombre', 'quality','ep_start','ep_end','paussed', 'skipped', )
        widgets = {
            'nombre': forms.TextInput(attrs={}),
            'paussed': forms.Select(attrs={},choices=CHOICES),
            'skipped': forms.Select(attrs={},choices=CHOICES),
        }
        
    
        
class SeriesFindForm(SeriesForm):
    to_saved = forms.BooleanField(initial=False, required=False)
    class Meta(SeriesForm.Meta):
        fields = SeriesForm.Meta.fields + ('to_saved',)
        
class TorrentServersForm(forms.ModelForm):
    
    
        plugins = forms.ModelMultipleChoiceField(queryset=Plugins.objects.all(),widget=forms.CheckboxSelectMultiple,required=False,)
    
        '''
        torrent_active = models.NullBooleanField(default=False)  # Field name made lowercase.
        space_disk = models.IntegerField()
        host = models.CharField(blank=True, null=True, max_length=200)
        port = models.IntegerField()
        user = models.CharField(blank=True, null=True, max_length=200)
        password = models.CharField(blank=True, null=True, max_length=200)
        paused = models.NullBooleanField(default=False)  # Field name made lowercase.
        download = models.CharField(blank=True, null=True, max_length=200)
        '''
    

        class Meta:
            model = TorrentServers
            fields = ('torrent_active', 'space_disk','host','port','user', 'password', 'paused','download','plugins' )
            widgets = {
                'torrent_active': forms.Select(attrs={},choices=CHOICES),
                'space_disk':forms.NumberInput(attrs={}),
                'host': forms.TextInput(attrs={}),
                'port':forms.NumberInput(attrs={}),
                'user': forms.TextInput(attrs={}),
                'password':forms.PasswordInput(render_value = True,attrs={}),
                'paused': forms.Select(attrs={},choices=CHOICES),
                'download': forms.TextInput(attrs={}),
            }

class TelegramSendForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    msg = forms.CharField(max_length=200, widget=forms.Textarea(attrs={}),  label="Mensaje", required=False,)
    receiver = forms.ChoiceField(choices=(), widget=forms.Select(attrs={'class':'form-control'}),label="Destinatarios", required=False)
    receiverUnique =  forms.CharField(max_length=20, widget=forms.TextInput(attrs={}), label="Destinatario",required=False,)


    def __init__(self, *args, **kwargs):
        
        EXTRA_CHOICES = [
            ('', '----'),
            ('ALL', 'All User'),
            # ('LP', 'Live Promotions'),
            # ('CP', 'Completed Promotions'),
        ]
        
        super(TelegramSendForm, self).__init__(*args, **kwargs)
        choices = [(pt.id, unicode(pt)) for pt in TelegramChatIds.objects.all()]
        choices.extend(EXTRA_CHOICES)
        self.fields['receiver'].choices = choices
    
    
    
    

    