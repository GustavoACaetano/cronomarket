<template>
    <section class="bg-gray-100 w-full flex items-center justify-center">
        <div class="flex items-center flex-col pb-24 md:w-7xl px-5 pt-10">
            <h1 class="text-5xl mb-18 text-center">
                Perguntas frequentes
            </h1>            

            <div class="flex flex-col gap-y-5 w-full">
                <details class="collapse collapse-arrow border border-base-300" name="my-accordion-det-1" >
                    <summary class="collapse-title font-semibold">
                        <span class="p-2">1.</span>
                        Como eu faço uma aposta em uma previsão?
                    </summary>
                    <div class="collapse-content text-sm">
                        Você escolhe um evento disponível (por exemplo: “Vai chover amanhã em São Paulo?”), analisa as 
                        probabilidades e decide se quer apostar a favor (SIM) ou contra (NÃO). Depois, insere o valor que 
                        deseja apostar e confirma a transação.
                    </div>
                </details>
                <details class="collapse collapse-arrow border border-base-300" name="my-accordion-det-1">
                    <summary class="collapse-title font-semibold">
                        <span class="p-2">2.</span>
                        Como funcionam as probabilidades nesse tipo de site?
                    </summary>
                    <div class="collapse-content text-sm">
                        As probabilidades são baseadas na opinião coletiva dos usuários e variam conforme mais pessoas 
                        apostam. Se muita gente acredita que algo vai acontecer, a chance (e o preço da aposta) sobe. 
                        Funciona como um “mercado”, onde oferta e demanda influenciam os valores.
                    </div>
                </details>
                <details class="collapse collapse-arrow border border-base-300" name="my-accordion-det-1">
                    <summary class="collapse-title font-semibold">
                        <span class="p-2">3.</span>
                        Quando e como eu recebo o dinheiro se eu ganhar?
                    </summary>
                    <div class="collapse-content text-sm">
                        Após o evento ser resolvido (ou seja, quando já se sabe o resultado real), o sistema distribui 
                        automaticamente os ganhos para quem acertou a previsão. O valor é creditado na sua conta dentro 
                        da plataforma.
                    </div>
                </details>
                <details class="collapse collapse-arrow border border-base-300" name="my-accordion-det-1">
                    <summary class="collapse-title font-semibold">
                        <span class="p-2">4.</span>
                        Posso retirar meu dinheiro a qualquer momento?
                    </summary>
                    <div class="collapse-content text-sm">
                        Você pode retirar o saldo disponível (não comprometido em apostas ativas) seguindo as regras de 
                        saque do site, que podem incluir taxas ou prazos de processamento.
                    </div>
                </details>
            </div>

            <div class="flex flex-col md:flex-row gap-y-4 items-center mt-10 gap-x-2 ">
                <p>Deseja enviar uma pergunta personalizada?</p>
                <textarea name="question" placeholder="Pergunta personalizada" id="question" class="textarea textarea-bordered md:textarea-md sm:textarea-lg bg-white textarea-neutral"></textarea>
                <button class="bg-black text-white px-8 py-3 ml-2 rounded-full text-base font-medium hover:bg-gray-800 transition-colors">Enviar</button>
            </div>
        </div>
    </section>
</template>