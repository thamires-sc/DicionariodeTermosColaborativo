from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, View, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q 
from django.contrib import messages
from .models import Termo, CATEGORIA_CHOICES
from .forms import TermoForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class ListaTermosView(ListView):
    model = Termo
    template_name = 'app/lista_termos.html' 
    paginate_by = 10 
    context_object_name = 'termos'
    ordering = ['termo'] 

    def get_queryset(self):
        queryset = super().get_queryset()
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(termo__icontains=query) | Q(definicao__icontains=query)
            ).distinct()
        
        categoria_filtro = self.request.GET.get('categoria')
        if categoria_filtro:
            queryset = queryset.filter(categoria=categoria_filtro)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CATEGORIA_CHOICES
        context['query_anterior'] = self.request.GET.get('q', '')
        context['categoria_anterior'] = self.request.GET.get('categoria', '')
        return context


# ----------------------------------------------
# 2. VISUALIZAÇÃO DE DETALHES (RF04)
# ----------------------------------------------

def detalhe_termo(request, pk):
    # RF04: Obtém o termo ou retorna 404
    termo = get_object_or_404(Termo, pk=pk)
    # RF04: Exibe título, definição completa e autor/colaborador
    return render(request, 'app/detalhe_termo.html', {'termo': termo})


# ----------------------------------------------
# 3. CRIAÇÃO DE TERMO (RF02, RRN03)
# ----------------------------------------------

# RF01/RF02: Requer que o usuário esteja logado
@method_decorator(login_required, name='dispatch')
class TermoCreateView(View):
    def get(self, request):
        # Exibe o formulário vazio
        form = TermoForm()
        return render(request, 'app/termo_form.html', {'form': form, 'acao': 'Adicionar'})

    def post(self, request):
        form = TermoForm(request.POST)
        if form.is_valid():
            termo = form.save(commit=False)
            # RRN03: Autoria Automática (preenche o colaborador com o usuário logado)
            termo.colaborador = request.user 
            termo.save()
            messages.success(request, f"Termo '{termo.termo}' cadastrado com sucesso!")
            return redirect('detalhe_termo', pk=termo.pk)
            
        # Se o formulário for inválido (RRN02: menos de 20 caracteres na definição)
        return render(request, 'app/termo_form.html', {'form': form, 'acao': 'Adicionar'})

# RF02: Mapeamos a view de criação para a classe acima
adicionar_termo = TermoCreateView.as_view()


# ----------------------------------------------
# 4. EDIÇÃO DE TERMO (RF07)
# ----------------------------------------------

# RF07: Requer login e verifica se o usuário é o autor
@method_decorator(login_required, name='dispatch')
class TermoUpdateView(View):
    def get(self, request, pk):
        termo = get_object_or_404(Termo, pk=pk)
        
        # RF07: Restrição de Edição/Exclusão Própria
        if termo.colaborador != request.user:
            messages.error(request, "Você só pode editar termos que você mesmo cadastrou.")
            return redirect('detalhe_termo', pk=termo.pk)
            
        form = TermoForm(instance=termo)
        return render(request, 'app/termo_form.html', {'form': form, 'acao': 'Editar'})

    def post(self, request, pk):
        termo = get_object_or_404(Termo, pk=pk)
        
        # Verifica novamente se é o autor antes de salvar
        if termo.colaborador != request.user:
            messages.error(request, "Acesso negado.")
            return redirect('detalhe_termo', pk=termo.pk)

        form = TermoForm(request.POST, instance=termo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Termo '{termo.termo}' atualizado com sucesso!")
            return redirect('detalhe_termo', pk=termo.pk)
            
        return render(request, 'app/termo_form.html', {'form': form, 'acao': 'Editar'})

# RF07: Mapeamos a view de edição para a classe acima
editar_termo = TermoUpdateView.as_view()


# ----------------------------------------------
# 5. EXCLUSÃO DE TERMO (RF07)
# ----------------------------------------------

# RF07: Requer login e verifica se o usuário é o autor
@method_decorator(login_required, name='dispatch')
class TermoDeleteView(DeleteView):
    model = Termo
    template_name = 'app/termo_confirm_delete.html'
    success_url = reverse_lazy('lista_termos') # Redireciona para a lista após a exclusão
    context_object_name = 'termo'

    def get_object(self, queryset=None):
        # RF07: Verifica se o usuário logado é o autor do termo
        obj = super().get_object(queryset)
        if obj.colaborador != self.request.user:
            messages.error(self.request, "Você só pode excluir termos que você mesmo cadastrou.")
            # Se a verificação falhar, lança exceção para interromper
            raise Exception("Tentativa de exclusão não autorizada.") 
        return obj
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception:
            # Em caso de exceção (não autorizado), redireciona
            return redirect('lista_termos')

# RF07: Mapeamos a view de exclusão
excluir_termo = TermoDeleteView.as_view()

class CadastroView(CreateView):
    # Usa o formulário padrão do Django para criação de usuários
    form_class = UserCreationForm
    # Define o template que será usado (que criamos como login.html)
    template_name = 'registration/cadastro.html'
    # Após o cadastro bem-sucedido, redireciona para a página de login
    success_url = reverse_lazy('login')